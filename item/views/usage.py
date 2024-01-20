""" Usage views """
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from item.forms import UsageForm
from item.models import StockEntry


class UsageUpdateHtmxView(LoginRequiredMixin, View):
    """View to update usage for stock using HTMX."""

    form_class = UsageForm
    input_template = "usage/usage_htmx_input.html"
    updated_template = "usage/usage_htmx_updated.html"

    def dispatch(self, request, *args, **kwargs):
        """Get the stock object before processing the request"""
        self.stock_entry = get_object_or_404(StockEntry, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET requests: return the form to update usage."""
        form = self.form_class(initial={"used_unit": self.stock_entry.remaining_unit})
        return render(request, self.input_template, {"entry": self.stock_entry, "form": form})

    def post(self, request, *args, **kwargs):
        """Handle POST requests: update the stock after usage"""
        form = self.form_class(request.POST)
        context = {"entry": self.stock_entry, "form": form}
        if form.is_valid():
            usage_instance = form.save(commit=False)
            usage_instance.stock_entry = self.stock_entry
            usage_instance.used_by = request.user
            usage_instance.save()            
            if "HX-Request" in request.headers:
                return render(request, self.updated_template, context)
            messages.success(request, "Usage updated ...")
            next_url = form.data.get("next") or self.success_url
            return redirect(next_url)
        messages.error(request, "Error updating usage")
        return render(request, self.input_template, context)


class UsageQRUpdateView(UsageUpdateHtmxView):
    """View to update usage for stock."""

    form_class = UsageForm
    input_template = "usage/usage_qr_update.html"
