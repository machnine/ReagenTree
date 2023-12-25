"""delivery forms."""
from django import forms
from django.utils import timezone

from attachment.forms import AttachmentForm
from .models import Delivery, DeliveryAttachment


class DeliveryForm(forms.ModelForm):
    """DeliveryForm."""

    class Meta:
        model = Delivery
        fields = ["notes", "delivery_date"]
        widgets = {
            "delivery_date": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "notes": forms.TextInput(attrs={"class": "form-control"}),
        }

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
