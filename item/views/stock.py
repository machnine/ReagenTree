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

from delivery.models import Delivery
from location.models import Location
from item.models import Stock, Item
from item.forms import StockCreateForm, StockUpdateForm


class StockCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for Stock model"""

    model = Stock
    is_created = True
    form_class = StockCreateForm
    template_name = "item/stock_create.html"
    success_url = reverse_lazy("stock_list")

    def form_valid(self, form):
        # get the quantity
        quantity = form.cleaned_data.get("quantity")
        # get the item instance
        item = get_object_or_404(Item, id=form.cleaned_data.get("item").id)
        with transaction.atomic():
            stocks = []
            for n in range(quantity):
                stock = Stock(
                    item=item,
                    created_by=self.request.user,
                    created=timezone.now(),
                    ordinal_number=n + 1,
                    remaining_tests=item.tests,
                    remaining_volume=item.volume,
                    remaining_weight=item.weight,
                    remaining_volume_unit=item.volume_unit,
                    remaining_weight_unit=item.weight_unit,
                    **{
                        key: value
                        for key, value in form.cleaned_data.items()
                        if key not in ["quantity", "item"]
                    },
                )
                stocks.append(stock)
            Stock.objects.bulk_create(stocks)

        action_success = mark_safe(
            f"{self.model.__name__}: {quantity}x <i><b>{form.instance}</b></i> created successfully."
        )
        messages.success(self.request, action_success)
        # set the object attribute to the last stock created
        # to allow for the get_success_url method to work properly
        self.object = stocks[-1]
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        delivery_pk = self.request.GET.get("delivery")
        if delivery_pk:
            initial["delivery"] = get_object_or_404(Delivery, delivery_pk)
        return initial

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # retain the selected item, location
        # in the form if the form is invalid for better UX
        if "item" in form.cleaned_data:
            item = get_object_or_404(Item, pk=form.cleaned_data["item"].id)
            context["item_name"] = item.name
        if "location" in form.cleaned_data:
            location = get_object_or_404(Location, pk=form.cleaned_data["location"].id)
            context["location_name"] = location.name
        return self.render_to_response(context)


class StockUpdateView(
    LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView
):
    """Update view for Stock model"""

    model = Stock
    is_updated = True
    form_class = StockUpdateForm
    template_name = "item/stock_update.html"
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
    template_name = "item/stock_list.html"
    paginate_by = 16
    ordering = ["-created", "-ordinal_number"]


class StockDetailView(LoginRequiredMixin, DetailView):
    """Detail view for Stock model"""

    model = Stock
    context_object_name = "stock"
    template_name = "item/stock_detail.html"


class StockDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for Stock model"""

    model = Stock
    action_url = "stock_delete"
    success_url = reverse_lazy("stock_list")
