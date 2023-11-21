"""delivery forms."""
from django import forms
from django.utils import timezone

from .models import Delivery


class DeliveryForm(forms.ModelForm):
    """DeliveryForm."""

    class Meta:
        """Meta"""

        model = Delivery
        fields = ["delivery_date", "received_by", "notes"]
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "datetime-local"}),
        }

    def clean_delivery_date(self):
        """Clean delivery_date."""
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date and delivery_date > timezone.now():
            raise forms.ValidationError("Delivery date cannot be in the future.")
        return delivery_date
