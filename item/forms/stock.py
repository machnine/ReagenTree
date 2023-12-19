"""This module contains the forms for the item app."""
from django import forms
from django.utils import timezone

from delivery.models import Delivery
from item.models import Stock


stock_form_fields = [
    "delivery",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show deliveries from the last week
        within_one_week = timezone.now() - timezone.timedelta(weeks=1)
        self.fields["delivery"].queryset = Delivery.objects.filter(
            delivery_date__gte=within_one_week
        )

    def clean_expiry_date(self):
        """Validate that the expiry date is not in the past."""
        expiry_date = self.cleaned_data.get("expiry_date")
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date


class StockUpdateForm(forms.ModelForm):
    """Custom update form for the Stock model."""

    class Meta:
        model = Stock
        fields = stock_form_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_delivery = self.instance.delivery
        start_date = current_delivery.delivery_date - timezone.timedelta(days=3)
        end_date = min(
            current_delivery.delivery_date + timezone.timedelta(days=3), timezone.now()
        )

        self.fields["delivery"].queryset = Delivery.objects.filter(
            delivery_date__range=[start_date, end_date]
        )

    # def clean_expiry_date(self):
    # This is not implemented to allow for the expiry date to be in the past
