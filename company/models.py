""" Company models"""

from django.db import models
from django.urls import reverse

from core.mixins import TimeStampUserMixin


class Company(TimeStampUserMixin, models.Model):
    """Company model"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        """Return name of company"""
        return f"{self.name}"

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]


class Test(models.Model):
    name = models.CharField(max_length=100, unique=True)
