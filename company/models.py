""" Company models"""
from django.db import models


class Company(models.Model):
    """Company model"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        """Return name of company"""
        return f"<Company: {self.name}>"

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
