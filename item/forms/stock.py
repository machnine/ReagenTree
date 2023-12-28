"""This module contains the forms for the item app."""
from django import forms
from django.utils import timezone

from item.models import Stock


stock_form_fields = [
    "delivery_date",
    "item",
    "delivery_condition",
    "lot_number",
    "expiry_date",
    "location",
]


class StockCreateForm(forms.ModelForm):
    """Custom input form for the Stock model."""

    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = Stock
        fields = stock_form_fields

    def clean_expiry_date(self):
        """Validate that the expiry date is not in the past."""
        expiry_date = self.cleaned_data.get("expiry_date")
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date

    def clean_location(self):
        """Validate that the location is not empty."""
        location = self.cleaned_data.get("location")
        if not location:
            raise forms.ValidationError("Location is required.")
        return location


class StockUpdateForm(forms.ModelForm):
    """Custom update form for the Stock model."""

    class Meta:
        model = Stock
        fields = stock_form_fields
