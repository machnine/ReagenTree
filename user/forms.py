"""Custom user forms"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form"""

    username = forms.EmailField(
        label="Email", help_text="Please use a valid email address."
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_(
            """Your password must contain at least 8 characters. <br>
                Your password can’t be a commonly used password. <br>
                Your password can’t be entirely numeric."""
        ),
    )

    class Meta(UserCreationForm.Meta):
        """Meta class"""

        model = CustomUser
        fields = UserCreationForm.Meta.fields

    def clean_username(self):
        """Validate username must be an email address"""
        username = self.cleaned_data.get("username")
        if not EmailValidator(username):
            raise ValidationError(_("Enter a valid email address."))
        return username


class CustomAuthenticationForm(AuthenticationForm):
    """Custom user login form"""

    username = forms.EmailField(label="Email")

    class Meta:
        """Meta class"""

        model = CustomUser
        fields = ("username", "password")
