"""Custom user forms"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form"""

    class Meta(UserCreationForm.Meta):
        """Meta class"""

        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomAuthenticationForm(AuthenticationForm):
    """Custom user login form"""

    username = forms.EmailField(label="Email")

    class Meta:
        """Meta class"""

        model = CustomUser
        fields = ("username", "password")
