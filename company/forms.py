"""company forms"""

from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    """company form"""
    class Meta:
        """meta class"""
        model = Company
        fields = ('name', 'website', 'phone', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', "rows": "2"})