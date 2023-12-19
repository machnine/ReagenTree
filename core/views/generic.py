from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View


class ObjectDeleteHTMXView(View):
    """Generic HTMX view for deleting an object."""

    model = None
    template_name = None
    success_url = None

    def get_object(self, pk):
        """Return the object the view is displaying."""
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning an object delete form."""
        obj = self.get_object(kwargs["pk"])
        return render(request, self.template_name, {"object": obj})

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an object."""
        with transaction.atomic():
            obj = self.get_object(kwargs["pk"])
            obj.delete()
            messages.success(request, f"{obj} deleted successfully.")
        return redirect(self.success_url)
