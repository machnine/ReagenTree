"""Stock Item views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from delivery.models import Delivery

from item.models import StockItem, Item
from item.forms import StockItemForm


class StockItemCreateView(LoginRequiredMixin, CreateView):
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
            stock_item = StockItem(
                item=item,
                created_by=self.request.user,
                created=timezone.now(),
                ordinal_number=n + 1,
                **form.cleaned_data,
            )
            stock_item.save()
        # set the object attribute to the last stock item created
        # to allow for the get_success_url method to work properly
        self.object = stock_item
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        delivery_pk = self.request.GET.get("delivery")
        if delivery_pk:
            initial["delivery"] = get_object_or_404(Delivery, pk=delivery_pk)
        return initial

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return super().get_success_url()


class StockItemListView(LoginRequiredMixin, ListView):
    """List view for StockItem model"""

    model = StockItem
    context_object_name = "stockitems"
    template_name = "item/stockitem_list.html"


class StockItemDetailView(LoginRequiredMixin, DetailView):
    """Detail view for StockItem model"""

    model = StockItem
    context_object_name = "stockitem"
    template_name = "item/stockitem_detail.html"