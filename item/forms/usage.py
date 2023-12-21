"""usage forms"""
from django import forms

from item.models import Usage


class UsageForm(forms.ModelForm):
    """Usage form"""

    # used_quantity must be > 0
    used_quantity = forms.DecimalField(min_value=0.0)

    class Meta:
        model = Usage
        fields = ("used_quantity",)
