""" Mixins """
from django.contrib import messages
from django.utils.safestring import mark_safe


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

    # create or update flag
    is_created = False
    is_updated = False

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        action = "created" if self.is_created else "updated"
        if self.is_created:
            form.instance.created_by = self.request.user
        if self.is_updated:
            form.instance.last_updated_by = self.request.user
        response = super().form_valid(form)
        action_success = mark_safe(
            f"{self.model.__name__}: <i><b>{form.instance}</b></i> {action} successfully."
        )
        messages.success(self.request, action_success)
        return response
