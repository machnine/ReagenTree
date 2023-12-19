"""This module contains the forms for the item app."""
from django import forms

from attachment.forms import AttachmentForm
from item.models import Item, ItemAttachment


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
            "tests",
            "volume",
            "volume_unit",
            "weight",
            "weight_unit",
        ]

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        for field in ["name", "product_id", "tests", "volume", "weight", "description"]:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        for field in ["volume_unit", "weight_unit"]:
            self.fields[field].widget.attrs.update({"class": "form-select"})

        self.fields["description"].widget.attrs.update({"rows": 3})


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
