"""delivery forms."""
from django import forms
from django.utils import timezone

from user.models import CustomUser
from .models import Delivery


delivery_fields = [
    "notes",
    "delivery_date",
    "received_by",
]


class DeliveryForm(forms.ModelForm):
    """DeliveryForm."""

    class Meta:
        """Meta"""

        model = Delivery
        fields = delivery_fields
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["received_by"].queryset = CustomUser.objects.exclude(
            is_superuser=True
        )

    def clean_delivery_date(self):
        """Clean delivery_date."""
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date and delivery_date > timezone.now():
            raise forms.ValidationError("Delivery date cannot be in the future.")
        return delivery_date
