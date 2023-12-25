""" Usage views """
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import get_object_or_404, render

from item.forms import UsageForm
from item.models import Stock


class UsageUpdateHtmxView(LoginRequiredMixin, View):
    """View to update usage for stock using HTMX."""

    form_class = UsageForm
    input_template = "usage/usage_htmx_input.html"
    updated_template = "usage/usage_htmx_updated.html"

    def dispatch(self, request, *args, **kwargs):
        """Get the stock object before processing the request"""
        self.stock = get_object_or_404(Stock, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET requests: return the form to update usage."""
        form = self.form_class(initial={"used_unit": self.stock.remaining_unit})
        return render(request, self.input_template, {"stock": self.stock, "form": form})

    def post(self, request, *args, **kwargs):
        """Handle POST requests: update the stock after usage"""
        form = self.form_class(request.POST)
        context = {"stock": self.stock, "form": form}
        if form.is_valid():
            usage_instance = form.save(commit=False)
            usage_instance.stock = self.stock
            usage_instance.used_by = request.user
            usage_instance.save()
            return render(request, self.updated_template, context)
        return render(request, self.input_template, context)
