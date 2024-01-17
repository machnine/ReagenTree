""" form for inhouse reagents """

from django import forms

from item.models import InhouseReagent, ReagentComponent


class InhouseReagentForm(forms.ModelForm):
    """Form for inhouse reagents"""

    expiry_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))

    class Meta:
        model = InhouseReagent
        fields = (
            "name",
            "product_id",
            "description",
            "category",
            "lot_number",
            "expiry_date",
            "quantity",
            "quantity_unit",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ("name", "product_id", "description", "lot_number", "quantity", "expiry_date"):
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"rows": 2})
        self.fields["quantity_unit"].widget.attrs.update({"class": "form-select"})


class ReagentComponentForm(forms.ModelForm):
    """Form for reagent components"""

    class Meta:
        model = ReagentComponent
        fields = ("stock", "quantity", "quantity_unit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stock"].widget.attrs.update({"class": "form-control"})
        self.fields["quantity"].widget.attrs.update({"class": "form-control"})
        self.fields["quantity_unit"].widget.attrs.update({"class": "form-select"})

        if self.instance.pk:
            self.fields["stock"].initial = self.instance.stock
            self.fields["stock"].widget.attrs.update({"hidden": True})
