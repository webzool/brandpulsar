import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, 
    from the given email and password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'phone']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'email-js',
                'id': 'modal-email',
                'placeholder': 'Enter your email'
            }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'required-js',
                'id': 'modal-password',
                'placeholder': 'Enter your password'
            }))
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'id': 'modal-remember_me'
            }))

    error_messages = {
        'invalid_login': "*Please enter a correct email and password.\
                        Note that both fields may be case-sensitive.",
    }


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    name = forms.CharField(required=False)
    surname = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'profile_picture']


class PasswordResetForm(forms.ModelForm):
    """ Custom Password Reset Form.
        Request object initialized for checking request.user
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'old_password_mismatch': "Old password value didn`t match",
    }
    old_password = forms.CharField()
    second_password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if check_password(old_password, self.request.user.password):
            return old_password
        else:
            raise forms.ValidationError(
                self.error_messages['old_password_mismatch'],
                code='password_mismatch',
            )

    def clean_second_password(self):
        password = self.cleaned_data.get("password1")
        second_password = self.cleaned_data.get("password2")
        if password and second_password and password != second_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return second_password


# class PaymentMethodForm(forms.ModelForm):
#    error_messages = {
#        'card_number_length': _("Card number length must be 16 characters"),
#        'card_number_error': _("Card number is not valid"),
#        'end_date_error': _("End date is not valid"),
#        'ccv_error': _("CCV is not valid"),
#    }
#    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
#    class Meta:
#        model=PaymentMethod
#        exclude=['user']
   
#    def clean_card_number(self):
#        card_number = self.cleaned_data.get('card_number')
#        if len(card_number) != 16:
#            print(f"Card number len {len(card_number)}")
#            raise forms.ValidationError(
#                self.error_messages['card_number_length']
#            )
#        try:
#            bool(int(card_number))
#        except:
#            raise forms.ValidationError(
#                self.error_messages['card_number_error']
#            )
#        return card_number
   
#    def clean_end_date(self):
#        end_date = self.cleaned_data.get('end_date')
#        if end_date < datetime.date.today():
#            raise forms.ValidationError(
#                self.error_messages['end_date_error'],
#                code='end_date_error'
#            )
#        return end_date
   
#    def clean_ccv_number(self):
#        ccv_number = self.cleaned_data.get('ccv_number')
#        if len(str(ccv_number)) != 3:
#            raise forms.ValidationError(
#                self.error_messages['ccv_error'],
#                code='ccv_error'
#            )
#        return ccv_number