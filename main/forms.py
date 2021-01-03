from django import forms
from django.forms import Textarea, TextInput, EmailField

from .models import BankWire, Contact


class BankWireForm(forms.ModelForm):
    class Meta:
        model = BankWire
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'John', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Doe', 'class': 'form-control'}),
            'email': TextInput(attrs={'placeholder': 'Your e-mail', 'class': 'form-control'}),
            'phone': TextInput(attrs={'placeholder': 'Your phone number', 'class': 'form-control'}),
            'message': Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': 'Message', 'class': 'form-control'}),
        }
