""" form for inhouse reagents """

from django import forms
from item.models import InhouseReagent, ReagentComponent


class InhouseReagentForm(forms.ModelForm):
    """Form for inhouse reagents"""

    class Meta:
        model = InhouseReagent
        fields = ["name", "product_id", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "off", "placeholder": "Reagent name"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "rows": 2, "placeholder": "Reagent description"}
        )
        self.fields["product_id"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "off", "placeholder": "Assign reagent ID"}
        )


class ReagentComponentForm(forms.ModelForm):
    """Form for reagent components"""

    class Meta:
        model = ReagentComponent
        fields = ["stock", "quantity", "quantity_unit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stock"].widget.attrs.update({"class": "form-control"})
        self.fields["quantity"].widget.attrs.update({"class": "form-control"})
        self.fields["quantity_unit"].widget.attrs.update({"class": "form-control"})
