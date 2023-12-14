"""This module contains the forms for the item app."""
from django import forms
from django.utils import timezone
from delivery.models import Delivery

from attachment.forms import AttachmentForm

from .models import StockItem, ItemAttachment


stockitem_form_fields = [
    "delivery",
    "item",
    "delivery_condition",
    "lot_number",
    "expiry_date",
    "location",
]


class StockItemCreateForm(forms.ModelForm):
    """Custom input form for the StockItem model."""

    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = StockItem
        fields = stockitem_form_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show deliveries from the last week
        within_one_week = timezone.now() - timezone.timedelta(weeks=1)
        self.fields["delivery"].queryset = Delivery.objects.filter(
            delivery_date__gte=within_one_week
        )


class StockItemUpdateForm(forms.ModelForm):
    """Custom update form for the StockItem model."""

    class Meta:
        model = StockItem
        fields = stockitem_form_fields

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


class ItemAttachmentCreateForm(AttachmentForm):
    """Custom input form for the ItemAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = ItemAttachment
        fields = ("file", "name", "description")


class ItemAttachmentUpdateForm(AttachmentForm):
    """Custom update form for the ItemAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = ItemAttachment
        exclude = ("file",)
