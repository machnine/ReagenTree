"""Validation forms"""
from django import forms

from item.models import ReagentValidation


class ValidationForm(forms.ModelForm):
    """Validation form"""

    class Meta:
        model = ReagentValidation
        fields = ("status", "comments")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "form-select"})
        self.fields["comments"].widget.attrs.update({"class": "form-control", "rows": 2})
