"""url patterns for user app"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserProfileEdit,
    UserLogoutConfirmView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("login")), name="logout"),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    path("user/update/", UserProfileEdit.as_view(), name="user_update"),
    path("user/logout/", UserLogoutConfirmView.as_view(), name="user_logout"),
]
