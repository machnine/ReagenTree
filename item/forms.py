"""This module contains the forms for the item app."""
from django import forms
from django.utils import timezone


from attachment.forms import AttachmentForm
from delivery.models import Delivery

from .models import Item, StockItem, ItemAttachment


# Item forms
class ItemForm(forms.ModelForm):
    """Custom input form for the Item model."""

    class Meta:
        model = Item
        fields = [
            "name",
            "product_id",
            "description",
            "category",
            "manufacturer",
            "supplier",
        ]


# Item Attachment forms
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


# StockItem forms

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

    def clean_expiry_date(self):
        """Validate that the expiry date is not in the past."""
        expiry_date = self.cleaned_data.get("expiry_date")
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date


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

    # def clean_expiry_date(self):
    # This is not implemented to allow for the expiry date to be in the past
