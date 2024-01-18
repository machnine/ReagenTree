"""Custom user forms"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import MaxLengthValidator, RegexValidator

from .models import CustomUser


class CustomUserProfileMixin:
    """Mixin for custom user profile forms"""

    placeholders = {
        "username": "[A-z 0-9 and @.+-_] only. ≤150 characters.",
        "current_password": "Current Password.",
        "password1": "≥8 characters and not entirely numeric.",
        "password2": "Enter the same password as before, for verification.",
        "first_name": "First Name. ≤30 characters.",
        "last_name": "Last Name. ≤30 characters.",
        "email": "Your OUH e-Mail.",
        "initials": "Your initials. ≤3 characters",
    }

    def setup_field_widgets(self, form, exclude_fields=None):
        """form field widget setup"""
        exclude_fields = exclude_fields or []
        for field_name, placeholder in self.placeholders.items():
            if field_name in exclude_fields:
                continue

            widget_class = forms.TextInput

            if "password" in field_name:
                widget_class = forms.PasswordInput
            elif "email" in field_name:
                widget_class = forms.EmailInput

            form.fields[field_name].widget = widget_class({"placeholder": placeholder, "class": "form-control"})

    def setup_field_validators(self, form):
        """field validators"""
        name_validators = [
            RegexValidator(regex=r"^[a-zA-Z]*$", message="Name can only contain letters."),
            MaxLengthValidator(30, message="Name cannot be longer than 30 characters."),
        ]
        form.fields["first_name"].validators = name_validators
        form.fields["last_name"].validators = name_validators
        form.fields["initials"].validators = [
            MaxLengthValidator(3, message="Initials cannot be longer than 3 characters.")
        ]
        form.fields["email"].validators = [
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", message="Please enter a valid email address."
            ),
            MaxLengthValidator(50, message="Email cannot be longer than 50 characters."),
        ]

    # Common clean methods
    def clean_email(self):
        """Email must be part of the 'ouh.nhs.uk' domain."""
        email = self.cleaned_data.get("email")
        if "@ouh.nhs.uk" not in email.lower():
            raise forms.ValidationError("Email must be part of the 'ouh.nhs.uk' domain.")
        return email


class CustomUserCreationForm(CustomUserProfileMixin, UserCreationForm):
    """Custom user creation form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_field_widgets(self, exclude_fields=["current_password"])
        self.setup_field_validators(self)
        self.fields["username"].validators = [
            RegexValidator(
                regex=r"^[\w.@+-]+$", message="Username can only contain letters, numbers, and @/./+/-/_ characters."
            )
        ]

    def clean_password1(self):
        """Password must be at least 8 characters long and not entirely numeric."""
        password1 = self.cleaned_data.get("password1")

        # If password1 is not provided or is empty, skip the validation
        if not password1:
            return password1

        # Perform the validation if password1 is present
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if password1.isdigit():
            raise forms.ValidationError("Password cannot be entirely numeric.")

        return password1

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2", "first_name", "last_name", "email", "initials")


class UserProfileForm(CustomUserProfileMixin, forms.ModelForm):
    """Custom user profile form"""

    current_password = forms.CharField(label="Current Password", required=False)
    password1 = forms.CharField(label="New Password", required=False)
    password2 = forms.CharField(label="Confirm Password", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_field_widgets(self, exclude_fields=["username"])
        self.fields["current_password"].widget.attrs.update({"autocomplete": "off"})
        self.setup_field_validators(self)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        user = self.instance

        # Change password only if new password fields are provided
        if password1 or password2:
            # Check that both new password fields are filled out
            if not all([password1, password2]):
                err_message = "Both new password fields must be filled out."
                self.add_error("password1", err_message)
                self.add_error("password2", err_message)

            # Check if the new passwords match
            if password1 != password2:
                self.add_error("password2", "The two new passwords didn't match.")

            # Validate current password if new passwords are provided
            if current_password:
                if not user.check_password(current_password):
                    self.add_error("current_password", "Your current password was entered incorrectly.")
            else:
                self.add_error("current_password", "Your current password is required to set a new password.")

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "initials")


class CustomAuthenticationForm(AuthenticationForm):
    """Custom user login form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setting up custom widgets for all fields
        self.fields["username"].widget = forms.TextInput(attrs={"class": "form-control"})
        self.fields["password"].widget = forms.PasswordInput(attrs={"class": "form-control"})

    class Meta:
        model = CustomUser
        fields = ("username", "password")
