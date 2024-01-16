"""category forms"""

from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    """category form"""

    class Meta:
        """meta class"""

        model = Category
        fields = ("name", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows": "2"})
