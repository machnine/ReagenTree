""" Location forms """
from django import forms

from .models import Location


class LocationForm(forms.ModelForm):
    """Form for creating a Location."""

    class Meta:
        model = Location
        fields = ["name", "room", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["room"].widget.attrs["class"] = "form-select"
        self.fields["description"].widget.attrs.update({"class":"form-control", "rows":2})
