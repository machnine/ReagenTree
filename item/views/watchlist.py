""" views for watchlist """


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView

from core.mixins import SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView
from item.forms import WatchListCreateForm
from item.models import Stock, WatchList


class WatchListView(LoginRequiredMixin, ListView):
    """Watch list view."""

    template_name = "watchlist/watchlist_list.html"
    context_object_name = "watchlists"

    def get_queryset(self):
        """Return all watchlists."""
        return WatchList.objects.filter(notification=True, acknowledged=None)


class WatchListCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Watch list create view."""

    model = WatchList
    form_class = WatchListCreateForm
    template_name = "watchlist/watchlist_create.html"
    success_url = "watchlist"

    def form_valid(self, form):        
        stock_pk = self.request.GET.get("stock_pk")
        if stock_pk:
            form.instance.stock = get_object_or_404(Stock, pk=stock_pk)
            form.instance.created_by = self.request.user
        else:
            messages.error(self.request, f"Stock pk={stock_pk} not found")
            return super().form_invalid(form)
        return super().form_valid(form)


class WatchListDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete watch list"""

    model = WatchList
    action_url = "watchlist_delete"
    success_url = "watchlist"