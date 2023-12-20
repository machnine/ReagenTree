from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View

from core.mixins import SuccessUrlMixin


class ObjectDeleteHTMXView(SuccessUrlMixin, View):
    """Generic HTMX view for deleting an object."""

    model = None
    action_url = None    
    success_url = None
    template_name = "partials/object_delete_form.html"

    def get_success_url(self):
        """Return the URL to redirect to, after processing a valid form."""
        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return self.success_url

    def get_object(self, pk):
        """Return the object the view is displaying."""
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning an object delete form."""
        obj = self.get_object(kwargs["pk"])
        action_url = reverse_lazy(self.action_url, kwargs={"pk": obj.pk})
        return render(
            request, self.template_name, {"object": obj, "action_url": action_url}
        )

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an object."""
        with transaction.atomic():
            obj = self.get_object(kwargs["pk"])
            obj.delete()
            messages.success(request, f"{obj} deleted successfully.")
        return redirect(self.get_success_url())
