"""Custom user models"""
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model: best practice to extend the AbstractUser
    to create this model for future exensiability.
    """