""" forms for wathclist """

from django import forms

from item.models import WatchList


class WatchListCreateForm(forms.ModelForm):
    """Watch list create form."""

    class Meta:
        model = WatchList
        fields = ("threshold", "threshold_type")

    threshold = forms.DecimalField(label="Threshold", max_digits=10, decimal_places=1, min_value=0, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["threshold"].widget.attrs.update({"class": "form-control", "placeholder": "Stock warning threshold..."})
        self.fields["threshold_type"].widget.attrs.update({"class": "form-control"})
        self.fields["threshold_type"].initial = 'U'
