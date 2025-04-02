"""Notice Board Models"""

from django.conf import settings
from django.db import models
from django.urls import reverse  # Import the reverse function
from django.utils import timezone

USER = settings.AUTH_USER_MODEL


class Notice(models.Model):
    """
    Model to represent a notice board message.
    """

    IMPORTANCE_CHOICES = [
        ("LOW", "Low", "text-info"),  # Blue
        ("MEDIUM", "Medium", "text-warning"),  # Yellow
        ("HIGH", "High", "text-danger"),  # Red
        ("CRITICAL", "Critical", "text-dark bg-danger bg-opacity-75"),  # Black with red background
    ]

    message = models.TextField()
    expiry_date = models.DateField()
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="created_notices")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, null=True, related_name="updated_notices", blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    importance = models.CharField(max_length=10, choices=[(c[0], c[1]) for c in IMPORTANCE_CHOICES], default="MEDIUM")
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Notice: {self.message[:50]}..."

    def is_expired(self):
        """
        Check if the notice has expired.
        """
        return timezone.now().date() >= self.expiry_date

    def get_importance_color(self):
        """Return the color class for the importance level."""
        for choice in self.IMPORTANCE_CHOICES:
            if choice[0] == self.importance:
                return choice[2]
        return ""  # Default to no color if not found

    def get_absolute_url(self):
        """
        Returns the URL to access a particular notice instance.
        """
        return reverse("notice_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notice"
        verbose_name_plural = "Notices"
