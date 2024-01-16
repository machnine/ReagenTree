"""usage forms"""
from django import forms

from item.models import Unit, Usage


class UsageForm(forms.ModelForm):
    """Usage form"""

    used_quantity = forms.DecimalField(min_value=0.0)
    used_unit = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Usage
        fields = ("used_quantity", "used_unit")
