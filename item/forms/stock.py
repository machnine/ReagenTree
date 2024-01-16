""" Stock forms"""
from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from attachment.forms import AttachmentForm
from item.models import Stock, StockEntry
from item.models.stock import StockAttachment


class StockForm(forms.ModelForm):
    """Custom input form for the Stock model."""

    quantity = forms.IntegerField(min_value=1, initial=1, required=False)
    delivery_date = forms.DateField(
        initial=timezone.now().date, widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
    )
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))

    class Meta:
        model = Stock
        fields = ("item", "inhouse_reagent", "comments", "lot_number", "condition", "delivery_date", "expiry_date")

    def __init__(self, *args, **kwargs):
        """Override the init method to add the location field."""
        super().__init__(*args, **kwargs)
        self.fields["condition"].widget.attrs.update({"class": "form-select"})
        self.fields["comments"].widget.attrs.update({"rows": 1})

        for field in ["comments", "lot_number", "quantity", "expiry_date", "delivery_date"]:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        # exclude fields for update
        if self.instance.pk:
            self.fields.pop("item")
            self.fields.pop("inhouse_reagent")

    def clean_expiry_date(self):
        """Validate that the expiry date is not in the past."""
        expiry_date = self.cleaned_data.get("expiry_date")
        if self.instance.pk is None:
            # if the object is being created, then the expiry date cannot be in the past
            if expiry_date and expiry_date < timezone.now().date():
                raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date

    def clean_delivery_date(self):
        """ "Validate that the delivery date is not in the future."""
        delivery_date = self.cleaned_data.get("delivery_date")
        if delivery_date and delivery_date > timezone.now().date():
            raise forms.ValidationError("Delivery date cannot be in the future.")
        return delivery_date


# Stock entry forms
class StockEntryCreateForm(forms.ModelForm):
    """Custom input form for the StockEntry model."""

    class Meta:
        model = StockEntry
        fields = ["location"]

    def __init__(self, *args, **kwargs):
        """Override the init method to add the location field."""
        super().__init__(*args, **kwargs)
        self.fields["location"].widget.attrs.update({"class": "form-control"})


# Stock entry formset
StockEntryFormSet = inlineformset_factory(Stock, StockEntry, form=StockEntryCreateForm, extra=1, can_delete=False)


class StockEntryUpdateForm(forms.ModelForm):
    """ "Custom update form for the StockEntry model."""

    class Meta:
        model = StockEntry
        fields = ["location", "comments", "remaining_quantity", "remaining_unit"]

    def __init__(self, *args, **kwargs):
        """Override the init method to add the location field."""
        super().__init__(*args, **kwargs)
        for field in ["location", "comments", "remaining_quantity"]:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["comments"].widget.attrs.update({"rows": 1})
        self.fields["remaining_unit"].widget.attrs.update({"class": "form-select"})


# Stock Attachment forms
class StockAttachmentCreateForm(AttachmentForm):
    """Custom input form for the StockAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = StockAttachment
        fields = ("file", "name", "description")


class StockAttachmentUpdateForm(AttachmentForm):
    """Custom update form for the StockAttachment model."""

    class Meta(AttachmentForm.Meta):
        model = StockAttachment
        exclude = ("file",)
