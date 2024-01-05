"""Stock Item views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from core.mixins import SuccessUrlMixin, FormValidMessageMixin
from core.views.generic import ObjectDeleteHTMXView
from item.models.stock import StockEntry
from item.models import Stock
from item.forms import StockForm, StockEntryFormSet, StockEntryUpdateForm


class StockCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for Stock model"""

    model = Stock
    form_class = StockForm
    template_name = "stock/stock_create.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = (
            StockEntryFormSet(self.request.POST)
            if self.request.POST
            else StockEntryFormSet()
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        entries = context["entries"]

        with transaction.atomic():
            form.instance.created_by = self.request.user
            form.instance.last_updated_by = self.request.user
            self.object = form.save()  # Save Stock instance first
            # Get the quantity of entries from the form
            quantity = form.cleaned_data["quantity"]
            entries.instance = self.object  # Set the instance of the formset

            if entries.is_valid():
                location = entries.cleaned_data[0]["location"]
                for n in range(quantity):
                    # Create the StockEntry instances
                    entry = StockEntry(
                        location=location,
                        stock=self.object,
                        last_updated_by=self.request.user,
                        ordinal_number=n + 1,
                    )
                    entry.save()
                return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))


class StockUpdateView(
    LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView
):
    """Update view for Stock model"""

    model = Stock
    form_class = StockForm
    template_name = "stock/stock_update.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object  # The stock being updated
        if stock.item:
            context["item_name"] = stock.item.name
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class StockListView(LoginRequiredMixin, ListView):
    """List view for Stock model"""

    model = Stock
    context_object_name = "stocks"
    template_name = "stock/stock_list.html"
    paginate_by = 16
    ordering = ["-created"]


class StockDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for Stock model"""

    model = Stock
    action_url = "stock_delete"
    success_url = reverse_lazy("stock_list")


# StockEntry Views


class StockEntryUpdateView(
    LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView
):
    """Update view for the StockEntry model"""

    model = StockEntry
    form_class = StockEntryUpdateForm
    template_name = "stock/stock_entry_update.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_entry = self.object  # The stock entry being updated

        if stock_entry.location:
            context["location_name"] = stock_entry.location.name
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class StockEntryDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for StockEntry model"""

    model = StockEntry
    action_url = "stock_entry_delete"
    success_url = reverse_lazy("stock_list")
