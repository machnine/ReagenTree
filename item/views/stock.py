"""Stock Item views"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import SuccessUrlMixin, FormValidMessageMixin
from core.views.generic import ObjectDeleteHTMXView

from location.models import Location
from item.models import Stock, Item
from item.forms import StockCreateForm, StockEntryFormSet, StockUpdateForm


class StockCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for Stock model"""

    model = Stock
    form_class = StockCreateForm
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
            self.object = form.save()

            if entries.is_valid():
                entries.instance = self.object
                entries.last_updated_by = self.request.user
                entries.save()
                return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))


class StockUpdateView(
    LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView
):
    """Update view for Stock model"""

    model = Stock
    form_class = StockUpdateForm
    template_name = "stock/stock_update.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object  # The stock being updated

        if stock.item:
            context["item_name"] = stock.item.name
        if stock.location:
            context["location_name"] = stock.location.name
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


class StockDetailView(LoginRequiredMixin, DetailView):
    """Detail view for Stock model"""

    model = Stock
    context_object_name = "stock"
    template_name = "stock/stock_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.usages.all():
            context["in_use_date"] = (
                self.object.usages.order_by("used_date").first().used_date
            )
        return context


class StockDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for Stock model"""

    model = Stock
    action_url = "stock_delete"
    success_url = reverse_lazy("stock_list")
