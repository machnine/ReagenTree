"""Stock Item views"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView

from delivery.models import Delivery
from location.models import Location
from item.models import StockItem, Item
from item.forms import StockItemCreateForm, StockItemUpdateForm


class StockItemCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for StockItem model"""

    model = StockItem
    form_class = StockItemCreateForm
    template_name = "item/stockitem_create.html"
    success_url = reverse_lazy("stock_list")

    def form_valid(self, form):
        # get the quantity
        quantity = form.cleaned_data.get("quantity")
        # get the item instance
        item = get_object_or_404(Item, form.cleaned_data.get("item").id)
        with transaction.atomic():
            stockitems = []
            for n in range(quantity):
                stockitem = StockItem(
                    item=item,
                    created_by=self.request.user,
                    created=timezone.now(),
                    ordinal_number=n + 1,
                    **{
                        key: value
                        for key, value in form.cleaned_data.items()
                        if key not in ["quantity", "item"]
                    },
                )
                stockitems.append(stockitem)
            StockItem.objects.bulk_create(stockitems)

        messages.success(
            self.request, f"{quantity} stock item(s) successfully created."
        )
        # set the object attribute to the last stock item created
        # to allow for the get_success_url method to work properly
        self.object = stockitems[-1]
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
            item = get_object_or_404(Item, form.cleaned_data["item"].id)
            context["item_name"] = item.name
        if "location" in form.cleaned_data:
            location = get_object_or_404(Location, pk=form.cleaned_data["location"].id)
            context["location_name"] = location.name
        return self.render_to_response(context)


class StockItemUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """Update view for StockItem model"""

    model = StockItem
    form_class = StockItemUpdateForm
    template_name = "item/stockitem_update.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stockitem = self.object  # The stock item being updated

        if stockitem.item:
            context["item_name"] = stockitem.item.name
        if stockitem.location:
            context["location_name"] = stockitem.location.name
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Stock Item successfully updated.")
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class StockItemListView(LoginRequiredMixin, ListView):
    """List view for StockItem model"""

    model = StockItem
    context_object_name = "stockitems"
    template_name = "item/stockitem_list.html"
    paginate_by = 16
    ordering = "-created"


class StockItemDetailView(LoginRequiredMixin, DetailView):
    """Detail view for StockItem model"""

    model = StockItem
    context_object_name = "stockitem"
    template_name = "item/stockitem_detail.html"


class StockItemDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for StockItem model"""

    model = StockItem
    template_name = "item/stockitem_delete_form.html"
    success_url = reverse_lazy("stock_list")
