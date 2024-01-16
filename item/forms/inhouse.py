""" form for inhouse reagents """

from django import forms

from item.models import InhouseReagent, ReagentComponent


class InhouseReagentForm(forms.ModelForm):
    """Form for inhouse reagents"""

    class Meta:
        model = InhouseReagent
        fields = ("name", "product_id", "description", "category", "lot_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 2})


class ReagentComponentForm(forms.ModelForm):
    """Form for reagent components"""

    class Meta:
        model = ReagentComponent
        fields = ("stock", "quantity", "quantity_unit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
