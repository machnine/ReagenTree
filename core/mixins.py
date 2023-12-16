""" Mixins """
from django.contrib import messages


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

    form_valid_message = ""
    # create or update flag
    is_created = False
    is_updated = False

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if self.is_created:
            form.instance.created_by = self.request.user
        if self.is_updated:
            form.instance.last_updated_by = self.request.user
        response = super().form_valid(form)
        if self.form_valid_message:
            messages.success(self.request, self.form_valid_message)
        return response
