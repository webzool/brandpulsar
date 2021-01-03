import django_filters
from django import forms
from django.db import models
from .models import Domain


class DomainFilter(django_filters.FilterSet):
    # price = django_filters.NumberFilter()
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='PRICE', widget=forms.TextInput(attrs={'placeholder': 'Min', 'class': 'price-max'}))
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='', widget=forms.TextInput(attrs={'placeholder': 'Max', 'class': 'price-min'}))
    length_gt = django_filters.NumberFilter(field_name='length', lookup_expr='gt', label='LENGTH', widget=forms.TextInput(attrs={'placeholder': 'Min', 'class': 'length-max'}))
    length_lt = django_filters.NumberFilter(field_name='length', lookup_expr='lt', label='', widget=forms.TextInput(attrs={'placeholder': 'Max', 'class': 'length-min'}))
    name = django_filters.CharFilter(lookup_expr='contains', label='CONTAINS', widget=forms.TextInput(attrs={'placeholder': 'Search place', 'class': 'contains'}))
