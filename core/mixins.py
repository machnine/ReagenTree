""" Mixins """
from django.conf import settings
from django.contrib import messages
from django.db import models
from django.utils.safestring import mark_safe

USER = settings.AUTH_USER_MODEL


class SuccessUrlMixin:
    """Success Url Mixin"""

    def get_success_url(self):
        """return the URL to redirect to, after processing a valid form."""

        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return super().get_success_url()


class FormValidMessageMixin:
    """Form Valid Message Mixin"""

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        action = "updated"
        if not bool(form.instance.pk):
            action = "created"
            form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        response = super().form_valid(form)
        action_success = mark_safe(f"{self.model.__name__}: <i><b>{form.instance}</b></i> {action} successfully.")
        messages.success(self.request, action_success)
        return response


class TimeStampUserMixin(models.Model):
    """TimeStamp User Mixin"""

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="created_%(class)s")
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="updated_%(class)s")
