"""This module contains the forms for the item app."""
from django import forms
from django.utils import timezone

from item.models import Stock


class StockCreateForm(forms.ModelForm):
    """Custom input form for the Stock model."""

    quantity = forms.IntegerField(min_value=1, initial=1)
    delivery_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Stock
        fields = ["item", "comments", "lot_number", "condition"]

    def __init__(self, *args, **kwargs):
        """Override the init method to add the location field."""
        super().__init__(*args, **kwargs)
        for field in [
            "comments",
            "lot_number",
            "quantity",
            "expiry_date",
            "delivery_date",
        ]:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["condition"].widget.attrs.update({"class": "form-select"})
        self.fields["comments"].widget.attrs.update({"rows": 2})

    def clean_expiry_date(self):
        """Validate that the expiry date is not in the past."""
        expiry_date = self.cleaned_data.get("expiry_date")
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date


class StockUpdateForm(forms.ModelForm):
    """Custom update form for the Stock model."""

    class Meta:
        model = Stock
        fields = ["item", "comments", "lot_number", "condition"]
