from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, FormView, DeleteView
from django.utils import timezone
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView
)
from users.models import  Favourites, PaymentHistory
from users.forms import (
    RegisterForm,
    LoginForm,
    UserEditForm,
    PasswordResetForm
)
from main.models import Plan
from users.utils import account_activation_token
from brandpulsar.utils.helpers import send_mail_helper
import stripe
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

stripe.api_key = settings.STRIPE_SECRET_KEY



User = get_user_model()


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().get(request, *args, **kwargs)

    def generate_mail(self, form, user):
        subject="Welcome to Brandpulsar"
        args = {
            'user': user,
            'email': user.email,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        email_context = {
            'user': user,
            'email': user.email,
            'first_name': form.cleaned_data.get("name"),
            'last_name': form.cleaned_data.get("surname"),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        html_ = get_template("emails/activation.html").render(email_context)

        message = Mail(
            from_email='Brandpulsar <info@brandpulsar.com>',
            to_emails=user.email,
            subject=subject,
            html_content=html_)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e)

    def form_valid(self, form):
        user = form.instance
        user.set_password(form.cleaned_data.get("password1"))
        customer = stripe.Customer.create(
            description="Customer created on sign up",
            email=form.cleaned_data.get("email")
        )
        user.stripe_id = customer.id
        user.save()
        self.generate_mail(user=user, form=form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:register-done-view')


class ActivateView(TemplateView):
    template_name = "pages/activate.html"

    def activate(self):
        try:
            uid = force_text(
                urlsafe_base64_decode(
                    self.kwargs.get('uidb64')
                ))
            user = get_object_or_404(
                User.objects.all(), pk=uid
            )
            token = account_activation_token.check_token(
                user, self.kwargs.get('token')
            )
            if user and token:
                user.is_active = True
                user.save()
                return True
        except:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = {
            'activated': 'Your account has been activated',
            'not_permitted': 'Not permitted. Please try again.',
            'register_done': 'Activation link has been sent to your email.',
        }
        if kwargs.get('uidb64'):
            activated = self.activate()
            context['message'] = messages.get('not_permitted')
            if activated:
                context['message'] = messages.get('activated')
        else:
            context['message'] = messages.get('register_done')
        return context


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().get(request, *args, **kwargs)
    
    def create_favourites(self, user):
        # Creates Favourites instance for those
        # who has not favourites yet.
        return Favourites.objects.get_or_create(
            defaults={'user':user})

    def form_valid(self, form):
        user = form.get_user()
        user.last_sign_in_ip = user.current_sign_in_ip
        user.sign_in_count += 1
        user.current_sign_in = timezone.now()
        user.current_sign_in_ip = self.request.META.get('REMOTE_ADDR')
        user.save()
        self.create_favourites(user=user)
        return super().form_valid(form)


class LogOutView(LogoutView):
    next_page = 'main:index'

    def post(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super().post(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password-reset.html"
    success_url = reverse_lazy('main:index')
    email_template_name = 'emails/password_reset_email.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password-reset-confirm.html"
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password-reset-done.html"


class UserEditView(FormView):
    template_name = 'users/user_edit.html'
    form_class = UserEditForm

    def generate_mail(self, form, user):
        subject = "New email verification"
        args = {
            'user': user,
            'email': form.cleaned_data.get("email"),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }

        email_context = {
            'user': user,
            'email': user.email,
            'first_name': user.name,
            'last_name': user.surname,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        html_ = get_template("emails/email_update.html").render(email_context)
        message = Mail(
            from_email='Brandpulsar <info@brandpulsar.com>',
            to_emails=args.get('email'),
            subject=subject,
            html_content=html_)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e)

    def form_valid(self, form):
        obj = self.request.user

        # User should verify new email address.
        if form.cleaned_data.get('email'):
            obj.is_active = False
            messages.success(self.request, "We just sent you an activation email")
            self.generate_mail(user=obj, form=form)
        elif form.cleaned_data.get('name') or form.cleaned_data.get('surname'):
            messages.success(self.request, "Changes saved")

        for k, v in form.cleaned_data.items():
            if form.cleaned_data.get(k):
                setattr(obj, k, v)

        obj.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['payment_methods'] = self.get_payment_method_list()
        return context

    def get_success_url(self):
        return reverse('users:user-edit-view')

    #def get_payment_method_list(self):
        #return PaymentMethod.objects.filter(user=self.request.user)


class UserPasswordEditView(FormView):
    template_name = 'users/user_edit_password.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        obj = self.request.user
        obj.set_password(form.cleaned_data.get("password"))
        obj.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('users:user-edit-password-view')


# class PaymentMethodListView(TemplateView):
#     template_name = 'users/payment_method_list.html'

#     #def get_payment_method_list(self):
#     #    return PaymentMethod.objects.filter(user=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #context['payment_methods'] = self.get_payment_method_list()
#         return context


# class PaymentMethodCreateView(FormView):
#    template_name = 'users/add_payment_method.html'
#    form_class = PaymentMethodForm

#    def form_valid(self, form):
#        instance = PaymentMethod.objects.create(
#            user=self.request.user,
#            name=form.cleaned_data.get("name"),
#            card_number=form.cleaned_data.get("card_number"),
#            holder_name=form.cleaned_data.get("holder_name"),
#            end_date=form.cleaned_data.get("end_date"),
#            ccv_number=form.cleaned_data.get("ccv_number")
#        )
#        return super().form_valid(form)

#    def get_success_url(self):
#        return reverse('main:index')


# class PaymentMethodUpdateView(FormView):
#    template_name = 'users/update_payment_method.html'
#    form_class = PaymentMethodForm

#    def get_object(self):
#        return get_object_or_404(
#            PaymentMethod.objects.all(),
#            user=self.request.user, pk=self.kwargs.get("pk")
#        )

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['instance'] = self.get_object()
#        return context

#    def form_valid(self, form):
#        instance = self.get_object()
#        name = form.cleaned_data.get("name")
#        if name:
#            instance.name = name
#        card_number = form.cleaned_data.get("card_number")
#        if card_number:
#            instance.card_number = card_number
#        holder_name = form.cleaned_data.get("holder_name")
#        if holder_name:
#            instance.holder_name = holder_name
#        end_date = form.cleaned_data.get("end_date")
#        if end_date:
#            instance.end_date = end_date
#        ccv_number = form.cleaned_data.get("ccv_number")
#        if ccv_number:
#            instance.ccv_number = ccv_number
#        instance.save()
#        return super().form_valid(form)

#    def get_success_url(self):
#        return reverse('users:dashboard')


# class PaymentMethodDeleteView(DeleteView):
#    model = PaymentMethod
#    template_name = "users/delete_payment_method.html"

#    def get_object(self, queryset=None):
#        return get_object_or_404(
#            self.model.objects.all(),
#            user=self.request.user, pk=self.kwargs.get("pk")
#        )

#    def get_success_url(self):
#        return reverse('main:index')


# class PaymentHistoryView(View):
#     def get(self, request, *args, **kwargs):
#         user = self.request.user
#         payment_history_list = PaymentHistory.objects.filter(user=user)
#         template_name = 'users/payment-history.html'
#         context = {
#             'user': user,
#             'payments' : PaymentHistory.objects.filter(user=user),
#             # Meta Tags
#             'title': 'Brandpulsar - Payment History',
#             'meta_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
#             'og_title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
#             'og_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
#             'og_type': 'website',
#             'og_url': 'https://brandpulsar.com/users/payment-history',
#             'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
#             'og_site': 'Brandpulsar'
#         }

#         return render(request, template_name=template_name, context=context)


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        template_name = 'users/dashboard.html'
        context = {
            'user': user,
            # Meta Tags
            'pub_key': settings.STRIPE_PUBLISHABLE_KEY,
            'title': 'Brandpulsar - Dashboard',
            'meta_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_title': 'Brandpulsar - The Finest Way of Finding Your Dream Domain!',
            'og_description': 'Find and buy a domain name for your business with a complete logo and design concepts all in one package regardless of your industry.',
            'og_type': 'website',
            'og_url': 'https://brandpulsar.com/users/dashboard',
            'og_image': 'https://brandpulsar.com/static/images/brandpulsar-og.png',
            'og_site': 'Brandpulsar'
        }

        return render(request, template_name=template_name, context=context)