"""Stock Item views"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from core.mixins import SuccessUrlMixin

from delivery.models import Delivery

from item.models import StockItem, Item
from item.forms import StockItemForm


class StockItemCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for StockItem model"""

    model = StockItem
    form_class = StockItemForm
    template_name = "item/stockitem_create.html"
    success_url = reverse_lazy("stock_list")

    def form_valid(self, form):
        # get the quantity
        quantity = form.cleaned_data.get("quantity")
        # get the item instance
        item = form.cleaned_data.get("item")
        item = Item.objects.get(pk=item.pk)
        # remove fields that are not part of the StockItem model or that are manually set
        del form.cleaned_data["quantity"]
        del form.cleaned_data["item"]

        for n in range(quantity):
            stockitem = StockItem(
                item=item,
                created_by=self.request.user,
                created=timezone.now(),
                ordinal_number=n + 1,
                **form.cleaned_data,
            )
            stockitem.save()
        messages.success(
            self.request, f"{quantity} stock item(s) successfully created."
        )
        # set the object attribute to the last stock item created
        # to allow for the get_success_url method to work properly
        self.object = stockitem
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        delivery_pk = self.request.GET.get("delivery")
        if delivery_pk:
            initial["delivery"] = get_object_or_404(Delivery, pk=delivery_pk)
        return initial


class StockItemListView(LoginRequiredMixin, ListView):
    """List view for StockItem model"""

    model = StockItem
    context_object_name = "stockitems"
    template_name = "item/stockitem_list.html"
    paginate_by = 16


class StockItemDetailView(LoginRequiredMixin, DetailView):
    """Detail view for StockItem model"""

    model = StockItem
    context_object_name = "stockitem"
    template_name = "item/stockitem_detail.html"


class StockItemDeleteView(LoginRequiredMixin, View):
    """Delete view for StockItem model"""

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning a StockItem delete form."""
        stockitem = StockItem.objects.get(pk=kwargs["pk"])
        return render(
            request, "item/stockitem_delete_form.html", {"stockitem": stockitem}
        )

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting a StockItem."""
        stockitem = StockItem.objects.get(pk=kwargs["pk"])
        stockitem.delete()
        messages.success(request, "Stock Item deleted successfully.")
        return redirect("stock_list")


class StockItemUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """Update view for StockItem model"""

    model = StockItem
    fields = ["item", "delivery_condition", "lot_number", "expiry_date", "location"]
    template_name = "item/stockitem_update.html"
    success_url = reverse_lazy("stock_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Stock Item successfully updated.")
        return response
