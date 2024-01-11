""" parameter confirmation form for label printing """

from django import forms
from label.models import LabelSheet


class LabelPrintForm(forms.Form):
    """form for label printing"""

    label_sheet = forms.ModelChoiceField(
        queryset=LabelSheet.objects.all(), label="Label Sheet Type"
    )
    skipped_labels = forms.IntegerField(
        initial=0, label="Number of Labels to Skip", min_value=0
    )
