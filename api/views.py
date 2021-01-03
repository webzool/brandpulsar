from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from celery.result import ResultBase

from brandpulsar.utils.helpers import send_mail_helper, check_domain_txt_records
from main.models import Domain, Industry, Tag
from users.models import Favourites
from marketplace.models import EstimatedDomainPrice, BrainstormingKeywords
from marketplace.utils import get_domain_appraisal
from api.serializers import (
    TagReadSerialzier,
    IndustryReadSerializer,
    DomainSerializer,
    FavouritesSerializer,
    ContactsSerializer,
    DomainNegotiationSerializer,

)
from api.pagination import BrandpulsarPagination
from marketplace.tasks import (
    get_godaddy_estimation
)
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class DomainListView(ListAPIView):
    model = Domain.objects.filter(is_active='listed')
    serializer_class = DomainSerializer
    pagination_class = BrandpulsarPagination

    def get_queryset(self):
        """ There are 4 different use cases:
            1) Queryset returns domains by specific ids -> For favourites case
            2) Queryset returns domains by industry-> For single industry page
            2) Queryset returns domains by filter values -> For filtering case
            3) Queryset returns domains by sorting options -> For sorting case

            * BY DEFAULT: it returns domains by featured column and created data.
        """
        params = self.request.query_params
        q = params.get('sort')

        # 1) Gets spesific domains by ids
        if params.getlist('ids'):
            self.model = self.model.filter(pk__in=params.getlist('ids'))

        # 2) Gets industry id
        if params.get('industry'):
            self.model = self.model.filter(industry__pk=params.get('industry'))

        # 3) Gets domains list based on filter inputs
        filters = {
            'min_price': 'price__gte',
            'max_price': 'price__lte',
            'min_length': 'length__gte',
            'max_length': 'length__lte',
            'contains': 'name__icontains',
            'tags': 'tags__pk',
            'syllable': 'syllable',
        }
        lookup_query = {}
        for k, v in params.items():
            if filters.get(k):
                lookup_query.update({filters.get(k): v})
        model = self.model.filter(**lookup_query)

        # 4) Gets domains list based on sorting options
        types = {
            'featured': model.order_by('-featured', '-date_created'),
            'hottest': model.order_by('visitors'),
            'high-price': model.order_by('-price'),
            'low-price': model.order_by('price'),
            'recently-added': model.order_by('-date_created'),
            'least-recently-added': model.order_by('date_created'),
        }
        if types.get(q):
            return types.get(q)
        # BY DEFAULT
        return types.get('featured')


class UsersDomainsListView(DomainListView):
    """ Endpoint for request users domain list.
        Returns request users domains / For Dashboard View
    """
    model = Domain.objects.all()

    def get_queryset(self):
        model = self.model.filter(owner=self.request.user)
        filters = self.request.query_params.get('f')

        filter_values = {
            'available': model.filter(status='available'),
            'sold': model.filter(status='sold'),
            'listed': model.filter(is_active='listed'),
            'pending': model.filter(is_active='pending'),
            'featured': model.filter(featured=True),
        }
        for k, v in filter_values.items():
            if filters == k:
                model = v
        return model


class SingleDomainAPIView(APIView):
    serializer_class = DomainSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_object(self):
        return get_object_or_404(
            Domain.objects.all(),
            pk=self.kwargs.get('pk')
        )

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class SearchAutoCompleteView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get_industries(self, q):
        return Industry.objects.filter(name__icontains=q)[:5]

    def get_tags(self, q):
        return Tag.objects.filter(title__icontains=q)[:5]

    def get(self, request, *args, **kwargs):
        q = request.query_params.get('q')
        result = []
        if q:
            industries = self.get_industries(q)
            tags = self.get_tags(q)
            if industries:
                result += IndustryReadSerializer(industries, many=True).data
            if tags:
                result += TagReadSerialzier(tags, many=True).data
        return Response(data=result, status=status.HTTP_200_OK)


class FavouriteAPIView(APIView):
    serializer_class = FavouritesSerializer
    pagination_class = BrandpulsarPagination
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(Favourites.objects.all(), user=self.request.user)

    def validate_domain(self, data):
        return get_object_or_404(Domain.objects.all(), pk=data)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        data = request.query_params.get('d')
        if data:
            try:
                obj = self.get_object()
                obj.domains.add(self.validate_domain(data=data))
                obj.save()
                return Response(status=status.HTTP_200_OK)
            except:
                pass
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactsAPIView(APIView):
    serializer_class = ContactsSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        domain = get_object_or_404(
            Domain.objects.all(), pk=request.data.get('domain'))

        args = {
            'name': request.data.get('name'),
            'surname': request.data.get('surname'),
            'email': request.data.get('email'),
            'domain': domain.__str__(),
            'message': request.data.get('message'),
        }

        text_message = f"First Name: {args.get('name')} | \
        Last Name: {args.get('surname')} | \
        Email: {args.get('email')} | Domain: {args.get('domain')} | \
        Message: {args.get('message')}"

        subject = f"Contact with owner form {args.get('domain')}"

        message = Mail(
            from_email='Brandpulsar <info@brandpulsar.com>',
            to_emails=['elmar@webzool.com', 'mardan@webzool.com'],
            subject=subject,
            html_content=text_message)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class DomainBrainStormingAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    model = Domain.objects.filter(is_active='listed')
    serializer_class = DomainSerializer

    def get(self, request, *args, **kwargs):
        kw = request.query_params.getlist('q')
        limit = request.query_params.get('limit')
        industry = request.query_params.getlist('industry')
        if industry:
            industry = Industry.objects.filter(pk__in=industry)
        if kw:
            # We store all searched keywords.
            stored = BrainstormingKeywords.objects.filter(key=kw[0])
            if stored:
                item = stored.first()
                item.count += 1
                if industry:
                    for industry in industry:
                        item.industry.add(industry)
                item.save()
            else:
                if industry:
                    item = BrainstormingKeywords(key=kw[0])
                    item.save()
                    for industry in industry:
                        item.industry.add(industry)
                else:
                    BrainstormingKeywords.objects.create(key=kw[0])
            q = Q()
            for k in kw:
                q |= Q(name__icontains=k)
            domains = self.model.filter(q).distinct()
            if limit:
                domains = domains[:int(limit)]
            if industry:
                domains = domains.filter(industry=industry).distinct()
            serializer = self.serializer_class(domains, many=True).data
            return Response(data=serializer)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DomainAppraisalAPIView(APIView):
    """ Requests GoDaddy Appraisal API and returns
        estimated domain price.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        domain = request.query_params.get('d')
        if domain:
            result = get_domain_appraisal(domain=domain)
            return Response(data=result, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyDomainAPIView(APIView):
    # TODO: we need to implement celery delay option
    # and update domain status automatically.
    permission_classes = [permissions.AllowAny]
    serializer_class = DomainSerializer

    def get(self, request, *args, **kwargs):
        domain = request.query_params.get('d')
        if domain:
            name = domain.split('.')[0]
            obj = Domain.objects.filter(name=name).first()
            if obj:
                payload = self.serializer_class(obj)
                result = check_domain_txt_records(domain=domain)
                if result:
                    obj.is_active = 'pending'
                    obj.save()
                return Response(payload.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NegotiateContactAPIView(APIView):
    serializer_class = DomainNegotiationSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return get_object_or_404(
            Domain.objects.all(), pk=self.request.data.get('domain')
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        domain = self.get_object()
        args = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'domain': domain.__str__(),
            'phone': request.data.get('phone'),
            'price': request.data.get('price'),
            'message': request.data.get('message'),
        }

        text_message = f"First Name: {args.get('first_name')} | \
        Last Name: {args.get('last_name')} | \
        Email: {args.get('email')} | Domain: {args.get('domain')} | Price: {args.get('price')} | \
        Phone: {args.get('phone')} | Message: {args.get('message')}"

        subject = f"Negotiation request for {args.get('domain')}"

        # send_mail_helper(subject=args.get("domain"),
        #                  text_message=text_message, html_message=args)
        message = Mail(
            from_email='Brandpulsar <info@brandpulsar.com>',
            to_emails=['elmar@webzool.com', 'mardan@webzool.com'],
            subject=subject,
            html_content=text_message)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
