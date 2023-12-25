"""delivery forms."""
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from attachment.forms import AttachmentForm
from .models import Delivery, DeliveryAttachment


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
        User = get_user_model()
        self.fields["received_by"].queryset = User.objects.exclude(is_superuser=True)

    def clean_delivery_date(self):
        """Clean delivery_date."""
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date and delivery_date > timezone.now():
            raise forms.ValidationError("Delivery date cannot be in the future.")
        return delivery_date


# Delivery Attachment forms
class DeliveryAttachmentCreateForm(AttachmentForm):
    """Custom input form for the DeliveryAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = DeliveryAttachment
        fields = ("file", "name", "description")


class DeliveryAttachmentUpdateForm(AttachmentForm):
    """Custom update form for the DeliveryAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = DeliveryAttachment
        exclude = ("file",)
