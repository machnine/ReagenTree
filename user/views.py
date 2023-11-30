""" User Authentification Views """
from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import CustomUserCreationForm, CustomAuthenticationForm

# get the user model (it could be a custom one in this case)
User = get_user_model()


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

    def get(self, request, *args, **kwargs):
        """
        If the user is already logged in, redirect to the index page
        """
        if request.user.is_authenticated:
            next_page = request.GET.get("next", reverse("index"))
            return redirect(next_page)
        return super().get(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    """User Logout View"""

    next_page = reverse_lazy("login")


class UserProfileView(LoginRequiredMixin, DetailView):
    """User Profile View"""

    model = User
    template_name = "user/profile_view.html"
    context_object_name = "user"

    def get_object(self, queryset: models.QuerySet[Any] = None) -> models.Model:
        """Get the user object instead of a user specified by URL"""
        return self.request.user


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """User Profile Edit View"""

    model = User
    template_name = "user/profile_edit.html"
    fields = ["first_name", "last_name"]
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset: models.QuerySet[Any] = None) -> models.Model:
        """Get the user object instead of a user specified by URL"""
        return self.request.user
