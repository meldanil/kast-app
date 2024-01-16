from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Title, Address

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


input_css_class = "form-control"

class TitleSearchForm(forms.Form):
    isbn = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  input_css_class

class TitleForm(forms.ModelForm):
    # title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Title
        fields = ['isbn', 'cover', 'title', 'author', 'publisher', 'year', 'origin', 'language', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['author'].widget.attrs['placeholder'] = 'Author(s) name'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  input_css_class

    def clean_title(self):
        # Get the cleaned data for the 'title' field
        title = self.cleaned_data.get('title')

        # Add your custom validation logic here
        # For example, let's ensure the title is at least 5 characters long
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")

        # Return the cleaned title
        return title

    # You can add similar clean methods for other fields if needed

    # Additional customization can be added here if needed


# class CheckoutForm(forms.ModelForm):
#     name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

#     class Meta:
#         model = Address
#         fields = ['street_adress', 'apartment_address', 'country', 'zip']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['country'] = CountryField(blank_label='select country').formfield(required=False, widget=CountrySelectWidget)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] =  input_css_class



class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': input_css_class,
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

        
