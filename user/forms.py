"""Custom user forms"""
from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form"""

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Setting up custom widgets for all fields
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "[A-z 0-9 and @.+-_] only. ≤150 characters.",
            }
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "≥8 characters and not entirely numeric.",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the same password as before, for verification.",
            }
        )
        self.fields["first_name"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name. ≤30 characters.",
            }
        )
        self.fields["last_name"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name. ≤30 characters."}
        )
        self.fields["email"].widget = forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your OUH e-Mail."}
        )
        self.fields["initials"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your initials. ≤3 characters",
            }
        )
        # validators
        self.fields["username"].validators = [
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Username can only contain letters, numbers, and @/./+/-/_ characters.",
            )
        ]
        self.fields["first_name"].validators = [
            RegexValidator(
                regex=r"^[a-zA-Z]*$", message="First name can only contain letters."
            ),
            MaxLengthValidator(
                30, message="First name cannot be longer than 30 characters."
            ),
        ]
        self.fields["last_name"].validators = [
            RegexValidator(
                regex=r"^[a-zA-Z]*$", message="Last name can only contain letters."
            ),
            MaxLengthValidator(
                30, message="Last name cannot be longer than 30 characters."
            ),
        ]
        self.fields["initials"].validators = [
            MaxLengthValidator(
                3, message="Initials cannot be longer than 3 characters."
            )
        ]
        self.fields["email"].validators = [
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                message="Please enter a valid email address.",
            ),
            MaxLengthValidator(
                50, message="Email cannot be longer than 50 characters."
            ),
        ]

    # validation methods
    def clean_password1(self):
        """Password must be at least 8 characters long and not entirely numeric."""
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if password1.isdigit():
            raise forms.ValidationError("Password cannot be entirely numeric.")
        return password1

    def clean_email(self):
        """Email must be part of the 'ouh.nhs.uk' domain."""
        email = self.cleaned_data.get("email")
        if "@ouh.nhs.uk" not in email.lower():
            raise forms.ValidationError(
                "Email must be part of the 'ouh.nhs.uk' domain."
            )
        return email

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "initials",
        )


class CustomAuthenticationForm(AuthenticationForm):
    """Custom user login form"""

    class Meta:
        """Meta class"""

        model = CustomUser
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        # Setting up custom widgets for all fields
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your User Name."}
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Your Password."}
        )


class UserProfileForm(forms.ModelForm):
    """Custom user profile form"""

    class Meta:
        """Meta class"""

        model = CustomUser
        fields = ("first_name", "last_name", "email", "initials")
