"""usage forms"""
from django import forms

from item.models import Usage, Stock


class UsageForm(forms.ModelForm):
    """Usage form"""

    class Meta:
        model = Usage
        fields = ["used_tests", "used_weight", "used_volume"]
