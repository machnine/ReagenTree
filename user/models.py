"""Custom user models"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model: best practice to extend the AbstractUser
    to create this model for future exensiability.
    """
    initials = models.CharField(max_length=10, blank=True, unique=True)