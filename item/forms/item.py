"""This module contains the forms for the item app."""
from django import forms

from attachment.forms import AttachmentForm
from item.models import Item, ItemAttachment


# Item forms
class ItemForm(forms.ModelForm):
    """Custom input form for the Item model."""

    class Meta:
        model = Item
        fields = (
            "name",
            "product_id",
            "cas_number",
            "description",
            "category",
            "manufacturer",
            "supplier",
            "quantity",
            "quantity_unit",
        )

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        for field in ["name", "product_id", "quantity", "description", "cas_number"]:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["quantity_unit"].widget.attrs.update({"class": "form-select"})
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
