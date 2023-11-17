"""url patterns for user app"""
from django.urls import path

from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, UserProfileEdit

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    path("user/edit/", UserProfileEdit.as_view(), name="user_edit"),
]
