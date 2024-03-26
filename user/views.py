""" User Authentification Views """
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, UpdateView, View

from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserProfileForm

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
            messages.warning(request, "You are already logged in.")
            return redirect(next_page)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Called if the form is valid and a success message
        """
        username = form.cleaned_data.get("username")
        user = get_user_model().objects.get(username=username)
        display_name = user.first_name or user.username
        messages.success(self.request, mark_safe(f"Welcome back, <b>{display_name}</b>."))
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    """User Profile View"""

    model = get_user_model()
    template_name = "user/profile_view.html"
    context_object_name = "user"

    def get_object(self, queryset=None) -> models.Model:
        """Get the user object instead of a user specified by URL"""
        return self.request.user


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """User Profile Edit View"""

    model = get_user_model()
    template_name = "user/profile_edit.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("user_profile")

    def get_object(self, queryset=None) -> models.Model:
        """Get the user object instead of a user specified by URL"""
        return self.request.user

    def form_valid(self, form):
        """Save the user profile"""
        user = form.save(commit=False)
        password1 = form.cleaned_data.get("password1")

        # Update the password if a new one is provided
        if password1:
            user.set_password(password1)
            messages.success(self.request, "Your password has been updated successfully.")

        user.save()
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)


class UserLogoutConfirmView(View):
    """User Logout Confirm View"""

    def get(self, request, *args, **kwargs):
        """Logout confirmation"""
        return render(request, "user/logout.html")
