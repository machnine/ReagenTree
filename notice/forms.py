from django import forms
from django.utils import timezone

from .models import Notice


class NoticeForm(forms.ModelForm):
    """Form for creating and updating notices."""

    class Meta:
        model = Notice
        fields = ["message", "expiry_date", "importance"]
        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "message": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        """Set the default expiry date to one month from now and add form-control class."""
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Only set default for new notices
            self.fields["expiry_date"].initial = timezone.now().date() + timezone.timedelta(days=30)

        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

        # Add form-select class to importance field
        self.fields["importance"].widget.attrs.update({"class": "form-select"})

    def clean_expiry_date(self):
        """Validate that the expiry date is not in the past."""
        expiry_date = self.cleaned_data.get("expiry_date")
        if self.instance.pk is None:
            # if the object is being created, then the expiry date cannot be in the past
            if expiry_date and expiry_date < timezone.now().date():
                raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date
