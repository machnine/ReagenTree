""" User Authentification Views """
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm


class UserRegistrationView(CreateView):
    """User Registration View"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "user/register.html"

    def form_valid(self, form):
        """
        Save the new user - this overide the original method
        and add the user to the CustomUser model
        """
        form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    """User Login View"""

    form_class = CustomAuthenticationForm
    template_name = "user/login.html"
    next_page = reverse_lazy("index")


class UserLogoutView(LogoutView):
    """User Logout View"""

    next_page = reverse_lazy("login")
