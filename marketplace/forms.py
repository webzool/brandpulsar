from decimal import Decimal

from django import forms

from main.models import Domain, Industry


class DomainCreateForm(forms.ModelForm):
    price = forms.DecimalField()
    negotiable_price = forms.DecimalField(
        label="Lowest price",
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Minimum price for the domain. (Optional)'
    }))
    
    class Meta:
        model = Domain
        fields = [
            'name', 'extension', 'price',
            'negotiable_price', 'thumbnail_image',
            'owner'
        ]
    
    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
    
    def clean_owner(self):
        return self.request.user