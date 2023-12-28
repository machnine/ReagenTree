""" Reagent validation workflow tracking """

from django.conf import settings
from django.db import models


class ReagentValidation(models.Model):
    """Reagent validation workflow tracking"""

    VALIDATION_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("NOT_REQUIRED", "Not Required"),
    )

    status = models.CharField(
        max_length=15, choices=VALIDATION_CHOICES, default="PENDING"
    )
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="validator",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    validated = models.DateTimeField(auto_now_add=True)
    authorised_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="authoriser",
    )
    authorised = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.status} - {self.validated_by} - {self.validated}"

    class Meta:
        ordering = ["-validated"]
