"""Custom user models"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model: best practice to extend the AbstractUser to create this model for future exensiability.
    Permissions:
                is_superuser    is_staff   is_active
    superuser   1               1           1         - has all permissions
    supervisor  0               1           1         - has all permissions except admin
    user        0               0           1         - has normal permissions
    guest       0               0           0         - has no permissions (default)
    """
    is_active = models.BooleanField(default=False)
    initials = models.CharField(max_length=10, blank=True, unique=True)

    
    @property
    def is_supervisor(self):
        """Returns True if user is a supervisor"""
        return self.is_staff and self.is_active    