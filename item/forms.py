"""This module contains the forms for the item app."""
from django import forms
from django.utils import timezone
from delivery.models import Delivery

from attachment.forms import AttachmentForm

from .models import StockItem, ItemAttachment


class StockItemForm(forms.ModelForm):
    """Custom input form for the StockItem model."""

    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show deliveries from the last week
        within_one_week = timezone.now() - timezone.timedelta(weeks=1)
        self.fields["delivery"].queryset = Delivery.objects.filter(
            delivery_date__gte=within_one_week
        )

    class Meta:
        model = StockItem
        fields = [
            "delivery",
            "item",
            "delivery_condition",
            "lot_number",
            "expiry_date",
            "location",
        ]


class ItemAttachmentForm(AttachmentForm):
    """Custom input form for the ItemAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = ItemAttachment
        fields = ("file", "name", "description")
