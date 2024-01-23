"""Category models."""
from django.db import models
from django.urls import reverse

from core.mixins import TimeStampUserMixin


class Category(TimeStampUserMixin, models.Model):
    """Category model."""

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return category name."""
        return f"{self.name}"

    def get_verbose_name(self, plural=False):
        return self._meta.verbose_name_plural if plural else self._meta.verbose_name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
