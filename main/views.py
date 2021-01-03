import json
import socket
import requests
from decimal import Decimal
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormMixin, FormView
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from main.models import Domain, Industry, BankWire, BlogPost, BlogCategory, Contact, Plan, Faq, Customer, Tag
from .forms import BankWireForm, ContactForm
from .filters import DomainFilter

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


stripe.api_key = settings.STRIPE_SECRET_KEY
instalment_webhook_endpoint_secret = settings.STRIPE_INSTALMENT_WEBHOOK_ENPOINT_SECRET
featured_webhook_endpoint_secret = settings.STRIPE_FEATURED_WEBHOOK_ENPOINT_SECRET

class IndexView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'pages/index.html'
        featured_domains = Domain.objects.filter(featured=True)
        featured_industries = Industry.objects.filter(featured=True)

        context = {
            'domains': featured_domains,
            'industries': featured_industries,
            # Meta Tags
            'title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'meta_description': 'Brandpulsar is a collection of premium brand names, matching domains with ready-to-use logos and mock-up designs.',
            'og_title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'og_description': 'Brandpulsar is a collection of premium brand names, matching domains with ready-to-use logos and mock-up designs.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class RobotsTXT(View):
    def get(self, request, *args, **kwargs):
        template_name = 'robots.txt'
        return render(request, template_name=template_name)


class DomainList(TemplateView):
    template_name = 'pages/domains.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'industries': Industry.get_root_nodes(),
            'tags' : Tag.objects.all(),
            # Meta Tags
            'title': 'Brandpulsar | Domains',
            'meta_description': 'Discover all the domains on our website and choose the one that fits your business. Filter the results based on price and industry type.',
            'og_title': 'Brandpulsar | Domains',
            'og_description': 'Discover all the domains on our website and choose the one that fits your business. Filter the results based on price and industry type.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/domains/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        })
        return context


class IndustryListView(View):
    def get(self, request, *args, **kwargs):
        industries = Industry.get_root_nodes().order_by('-numchild')
        template_name = 'pages/industries.html'

        context = {
            'industries': industries,
            'template_name': template_name,
            # Meta Tags
            'title': 'Brandpulsar | Industries',
            'meta_description': 'Our premium domain names cover a wide range of business industries including education, marketing, eCommerce, video gaming, etc.',
            'og_title': 'Brandpulsar | Industries',
            'og_description': 'Our premium domain names cover a wide range of business industries including education, marketing, eCommerce, video gaming, etc.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/industries/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }
        return render(request, context=context, template_name=template_name)


class BlogListView(View):
    def get(self, request, *args, **kwargs):
        posts = BlogPost.objects.all().order_by('-date_created')
        paginator = Paginator(posts, 11)

        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        categories = BlogCategory.objects.all()
        current = "current-page"

        template_name = 'pages/blog.html'

        context = {
            'posts': posts,
            'categories': categories,
            'template_name': template_name,
            'current': current,
            # Meta Tags
            'title': 'Blog',
            'meta_description': 'Meta Description',
            'og_title': '',
            'og_type': 'website',
            'og_url': '',
            'og_image': '',
            'og_site': 'Brandpulsar'
        }

        return render(request, context=context, template_name=template_name)


@csrf_exempt
def ajax_favorite_view(request):
    if request.method == 'POST':
        domain_id = request.POST.get("domain_id")
        action = request.POST.get("action")
        if action == 'add':
            print('add')
            print("Domain id", domain_id)
            domain = Domain.objects.filter(pk=int(domain_id)).update(favorite_count=F('favorite_count') + 1)
        elif action == 'remove':
            print('remove')
            domain = Domain.objects.filter(pk=domain_id).update(favorite_count=F('favorite_count') - 1)

        data = {
            'domain': domain
        }
        
        return JsonResponse(data)
    elif request.method == 'GET':
        domain = request.GET.get('domain', None)
        domain_fav = Domain.objects.get(pk=domain)
        domain_fav_count = domain_fav.favorite_count
        data = {
            'domain': domain_fav_count
        }

        return JsonResponse(data)

    return domain_id


class FavoritesView(View):
    def get(self, request):
        template_name = 'pages/favourites.html'
        context = {
            # Meta Tags
            'title': 'Brandpulsar | Favorites',
            'meta_description': 'Browse through thousands of titles and collect your favourite domain names in on the Brandpulsar website without registration.',
            'og_title': 'Brandpulsar | Favorites',
            'og_description': 'Browse through thousands of titles and collect your favourite domain names in on the Brandpulsar website without registration.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/favorites/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }
        return render(request, template_name=template_name, context=context)


class SingleDomainView(DetailView):
    model = Domain
    count_hit = True
    template_name = "dynamic/single-domain.html"

    def track_visitors(self):
        # Tracks domain visitors bu unique ip address
        obj = self.get_object()
        obj.visit_count += 1
        obj.save()
        return obj

    def dispatch(self, request, *args, **kwargs):
        # Every time domain visitors table updates, when this page reloads.
        self.track_visitors()
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        return Domain.objects.prefetch_related(
            'tags').get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        domain = self.get_object()
        plans = Plan.objects.filter(domain=domain)
        context = super().get_context_data(**kwargs)
        context.update({
            'domain': domain,
            'plans': plans,
            'domain_slug': self.kwargs.get('slug'),
            'base_url': settings.BASE_URL,
            'pub_key': settings.STRIPE_PUBLISHABLE_KEY,
            # Meta Tags
            'title': f'Brandpulsar | {domain.__str__()}',
            'meta_description': f'Buy the premium domain name - {domain.name} with a complete package of its logo and design concepts & mock-ups on Brandpulsar.',
            'og_title': f'Brandpulsar | {domain.__str__()}',
            'og_description': f'Buy the premium domain name {domain.name} with a complete package of its logo and design concepts & mock-ups on Brandpulsar.',
            'og_type': 'article',
            'og_url': 'https://brandpulsar.com/domains/' + domain.slug,
            'og_image': 'https://brandpulsar.com' + domain.thumbnail_image.url,
            'og_site': 'Brandpulsar'
        })
        return context


class SingleBlogPostView(FormMixin, DetailView):
    model = BlogPost

    def get(self, request, slug):
        post = BlogPost.objects.get(slug=slug)
        # print(post.tags.all)
        if post.tags:
            for tag in post.tags.all():
                industry = None
                domain = None
                try:
                    industry = Industry.objects.get(slug=tag.name.lower())
                    domain = Domain.objects.filter(industry=industry)[:4]
                except Industry.DoesNotExist:
                    print("No")
        # domain = Domain.objects.filter(industry=industry)
        template_name = "dynamic/single-post.html"
        context = {
            'template_name': template_name,
            'post': post,
            'domains': domain,
            # Meta Tags
            'title': post.title,
            'meta_description': post.metadescription,
            'og_description': post.metadescription,
            'og_title': post.title,
            'og_type': 'article',
            'og_url': 'https://brandpulsar.com/blog/' + post.slug,
            'og_image': 'https://brandpulsar.com' + post.thumbnail_image.url,
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class SingleBlogCategoryView(View):
    def get(self, request, slug=None, *args, **kwargs):
        template_name = 'dynamic/single-category.html'

        try:
            category = BlogCategory.objects.get(slug=slug)
            posts = BlogPost.objects.filter(
                category=category).order_by('-date_created')
            paginator = Paginator(posts, 10)

            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            categories = BlogCategory.objects.all()

            context = {
                'category': category,
                'posts': posts,
                'categories': categories,
                # Meta Tags
                'title': 'Domains',
                'meta_description': 'Meta Description',
                'og_title': '',
                'og_type': 'website',
                'og_url': '',
                'og_image': '',
                'og_site': 'Brandpulsar'
            }

            return render(request, template_name=template_name, context=context)

        except BlogCategory.DoesNotExist:
            return render(request, template_name='404.html')


class Success(View):
    def get(self, request, *args, **kwargs):
        # template_name = 'pages/success.html'
        return render(request, template_name='pages/success.html')


# Using Django
@csrf_exempt
def instalment_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, instalment_webhook_endpoint_secret
        )
    except ValueError as e:

        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event.type == 'customer.subscription.created':
        customer_subscription = event.data.object
        # print('PaymentIntent was successful!', customer_subscription)
        schedule = stripe.SubscriptionSchedule.create(
            customer=customer_subscription.customer,
            start_date='now',
            end_behavior="cancel",
            phases=[
                {
                    "plans": [
                        {
                            "plan": customer_subscription.plan.id,
                            "quantity": 1,
                        },
                    ],
                    "iterations": customer_subscription.plan.nickname,
                },
            ],
        )
        # print("Schedule is: ", schedule)
    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)

@csrf_exempt
def featured_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, featured_webhook_endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        payment = event.data.object # contains a stripe.PaymentIntent
        # if payment.payment_status == 'paid':
        subscription = stripe.Subscription.retrieve(payment.subscription)
        domain_id = subscription.plan.id
        domain = Domain.objects.filter(featured_plan_id=domain_id).update(featured=True)
            
    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)


class TermsOfUse(View):
    def get(self, request, *args, **kwargs):
        # template_name = 'pages/success.html'
        return render(request, template_name='pages/terms-of-use.html')


class TermsOfService(View):
    def get(self, request, *args, **kwargs):
        # template_name = 'pages/success.html'
        return render(request, template_name='pages/terms-of-service.html')


class PrivacyPolicy(View):
    def get(self, request, *args, **kwargs):
        # template_name = 'pages/success.html'
        return render(request, template_name='pages/privacy-policy.html')


class HowItWorks(View):
    def get(self, request, *args, **kwargs):
        context = {
            # Meta Tags
            'title': 'Brandpulsar | How It Works',
            'meta_description': 'Learn how to get your first domain from Brandpulsar and see how our future partnership would look like to you.',
            'og_title': 'Brandpulsar | How It Works',
            'og_description': 'Learn how to get your first domain from Brandpulsar and see how our future partnership would look like to you.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/how-it-works/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }
        return render(request, context=context, template_name='pages/how-it-works.html')


class KnowledgeBase(View):
    def get(self, request, *args, **kwargs):
        # template_name = 'pages/success.html'
        return render(request, template_name='pages/knowledge-base.html')


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if data['paymentType'] == 'onetime':
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'name': data['product_name'],
                    'description': data['product_description'],
                    'images': [data['product_image']],
                    'amount': int(Decimal(data['product_price']) * 100),
                    'currency': 'usd',
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.BASE_URL + '/success/',
                cancel_url=settings.BASE_URL + '/cancel/',
            )
        elif data['paymentType'] == 'instalment':
            session = stripe.checkout.Session.create(
                success_url=settings.BASE_URL + "/success/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.BASE_URL + "/cancel/",
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": data['priceId'],
                        "quantity": 1
                    }
                ]
            )
        elif data['paymentType'] == 'featured':
            session = stripe.checkout.Session.create(
                success_url=settings.BASE_URL + "/success/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.BASE_URL + "/cancel/",
                payment_method_types=["card"],
                customer=request.user.stripe_id,
                mode="subscription",
                line_items=[
                    {
                        "price": data['priceId'],
                        "quantity": 1
                    }
                ]
            )
        data = {
            'id': session.id
        }
            
        return JsonResponse(data)


@csrf_exempt
def mark_as_featured(request):
        print('featured')
        domain_id = request.POST.get("domain_id")
        data = request.POST.get()
        print('data', data)
        print('domain id', domain_id)
        
        data = {
            'id': 'id'
        }
            
        return JsonResponse(data)


@csrf_exempt
def create_customer_portal_session(request):
    if request.method == 'POST':
        user = request.user
        portal = stripe.billing_portal.Session.create(
            customer=user.stripe_id,
            return_url=settings.BASE_URL + '/users/dashboard/',
        )
        data = {
            'portal': portal
        }
        return redirect(portal.url)



class Session(View):
    def get(self, request, *args, **kwargs):
        print("Session")
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'name': 'T-shirt',
                'description': 'Comfortable cotton t-shirt',
                'images': ['https://example.com/t-shirt.png'],
                'amount': 500,
                'currency': 'usd',
                'quantity': 1,
            }],
            success_url=settings.BASE_URL +
            'success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.BASE_URL + 'canceled/',
        )
        # template_name = 'pages/success.html'
        return render(request, template_name='pages/session.html')


class Canceled(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='pages/canceled.html')


class SingleIndustryView(View):
    def get(self, request, slug=None, *args, **kwargs):
        template_name = 'dynamic/single-industry.html'
        industry = Industry.objects.get(slug=slug)
        industry_list = [industry.pk, ]

        for child in industry.get_children():
            industry_list.append(child.pk)

            
        context = {    
            'industry': industry,
            "tags" : Tag.objects.all(),
            'insget': slug,
            # Meta Tags
            'title': 'Brandpulsar | ' + str(industry.name),
            'meta_description': 'If you are starting a business in ' + str(industry.name) + ' industry, this list of domains will be the strongest candidates to launching your brand.',
            'og_title': 'Brandpulsar | ' + str(industry.name),
            'og_description': 'If you are starting a business in ' + str(industry.name) + ' industry, this list of domains will be the strongest candidates to launching your brand.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/domains/industries/' + industry.slug,
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)

        


class ContactView(FormView):
    form_class = ContactForm
    template_name = "pages/contact.html"
    success_url = "/thank-you/"

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        email = form.cleaned_data['email']
        user_message = form.cleaned_data['message']
        mail_content = "<strong>New Contact Form Submitted</strong><br> First Name: {} <br>Last Name:  {}<br>Phone: {} <br>Email: {} <br>Message: {}".format(first_name, last_name, phone, email, user_message)

        Contact.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            message = user_message,
            phone = phone,
        )

        message = Mail(
            from_email='Brandpulsar <info@brandpulsar.com>',
            to_emails=['elmar@webzool.com', 'mardan@webzool.com'],
            subject='Brandpulsar Contact Page',
            html_content=mail_content)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e)

        return super(ContactView, self).form_valid(form)


class Faq(View):
    def get(self, request, *args, **kwargs):

        context = {
            # Meta Tags
            'title': 'Brandpulsar | FAQ',
            'meta_description': 'Discover the answers to frequently asked questions and learn more about our company and the process of buying a domain name.',
            'og_title': 'Brandpulsar | FAQ',
            'og_description': 'Discover the answers to frequently asked questions and learn more about our company and the process of buying a domain name.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/faq/',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }
        return render(request, context=context, template_name='pages/faq.html')


class Customers(View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        template_name = 'pages/customers.html'
        context = {
            'customers': customers,
            # Meta Tags
            'title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'meta_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'og_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/customers',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class SingleCustomer(DetailView):
    model = Customer

    def get(self, request, slug):
        customer = Customer.objects.get(slug=slug)
        
        template_name = "dynamic/single-customer.html"
        context = {
            'template_name': template_name,
            'customer': customer,
            # Meta Tags
            'title': customer.name,
            'meta_description': customer.description,
            'og_description': customer.description,
            'og_title': customer.name,
            'og_type': 'article',
            'og_url': 'https://brandpulsar.com/customers/' + customer.slug,
            'og_image': 'https://brandpulsar.com' + customer.thumbnail_image.url,
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class StartupNames(View):
    def get(self, request, *args, **kwargs):
        domains = Domain.objects.filter(featured=True)[:10]
        template_name = 'pages/business-names/startup-names.html'
        context = {
            'domains': domains,
            # Meta Tags
            'title': 'Brandpulsar - Startup Names',
            'meta_description': 'We offer attention-grabbing and creative startup names within the budget of newly established businesses.',
            'og_title': 'Brandpulsar - Startup names',
            'og_description': 'We offer attention-grabbing and creative startup names within the budget of newly established businesses.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/startup-names',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class WebsiteNames(View):
    def get(self, request, *args, **kwargs):
        domains = Domain.objects.filter(featured=True)[:10]
        template_name = 'pages/business-names/website-names.html'
        context = {
            'domains': domains,
            # Meta Tags
            'title': 'Brandpulsar - Website Names',
            'meta_description': 'Brandpulsar offers premium website names for individuals and businesses to help establish their online presence.',
            'og_title': 'Brandpulsar - Website Names',
            'og_description': 'Brandpulsar offers premium website names for individuals and businesses to help establish their online presence.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/website-names',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class DomainNames(View):
    def get(self, request, *args, **kwargs):
        domains = Domain.objects.filter(featured=True)[:10]
        template_name = 'pages/business-names/domain-names.html'
        context = {
            'domains': domains,
            # Meta Tags
            'title': 'Brandpulsar - Domain Names',
            'meta_description': 'Whether you are looking for a brandable, descriptive, short, or catchy domain, Brandpulsar has you covered!',
            'og_title': 'Brandpulsar - Domain Names',
            'og_description': 'Whether you are looking for a brandable, descriptive, short, or catchy domain, Brandpulsar has you covered!',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/domain-names',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class CompanyNames(View):
    def get(self, request, *args, **kwargs):
        domains = Domain.objects.filter(featured=True)[:10]
        template_name = 'pages/business-names/company-names.html'
        context = {
            'domains': domains,
            # Meta Tags
            'title': 'Brandpulsar - Company Names',
            'meta_description': 'Whether you have finance, marketing, hospitality, or any other company, we can offer a catchy domain name that perfectly fits your industry.',
            'og_title': 'Brandpulsar - Company Names',
            'og_description': 'Whether you have finance, marketing, hospitality, or any other company, we can offer a catchy domain name that perfectly fits your industry.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/company-names',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class HowToNameYourBrand(View):
    def get(self, request, *args, **kwargs):
        template_name = 'pages/on-page/how-to-name-your-brand.html'
        context = {
            # Meta Tags
            'title': 'Brandpulsar - How To Name Your Brand',
            'meta_description': 'If you want to learn what goes into finding a brand name for your newly established business, read on.',
            'og_title': 'Brandpulsar - How To Name Your Brand',
            'og_description': 'If you want to learn what goes into finding a brand name for your newly established business, read on.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/how-to-name-your-brand',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class WhatMakesaNameBrandable(View):
    def get(self, request, *args, **kwargs):
        template_name = 'pages/on-page/what-makes-a-name-brandable.html'
        context = {
            # Meta Tags
            'title': 'Brandpulsar - What Makes a Name Brandable',
            'meta_description': 'Learn what makes a name brandable and how you can come up with one and build it from scratch.',
            'og_title': 'Brandpulsar - What Makes a Name Brandable',
            'og_description': 'Learn what makes a name brandable and how you can come up with one and build it from scratch.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/what-makes-a-name-brandable',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


class ThankYou(View):
    def get(self, request, *args, **kwargs):
        template_name = 'pages/thank-you.html'
        context = {
            # Meta Tags
            'title': 'Brandpulsar - Thank You',
            'meta_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'og_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/thank-you',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)
