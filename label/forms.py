""" parameter confirmation form for label printing """

from django import forms
from label.models import LabelSheet


class LabelPrintForm(forms.Form):
    """form for label printing"""

    label_sheet = forms.ModelChoiceField(
        queryset=LabelSheet.objects.all(), label="Label sheet type", initial=0
    )
    skipped_labels = forms.IntegerField(
        initial=0, label="Number of labels to skip", min_value=0
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["label_sheet"].widget.attrs.update({"class": "form-select"})
        self.fields["skipped_labels"].widget.attrs.update({"class": "form-control"})
