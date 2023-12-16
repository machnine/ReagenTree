""" Location forms """
from django import forms

from .models import Location

class LocationForm(forms.ModelForm):
    """Form for creating a Location."""
    
    class Meta:
        model = Location
        fields = ["name", "room", "description"]