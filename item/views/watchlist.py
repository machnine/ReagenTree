""" views for watchlist """
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import CreateView, FormView, ListView

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


class WatchListAcknowledgeView(LoginRequiredMixin, SuccessUrlMixin, FormView):
    """Acknowledge watch list."""

    model = WatchList
    template_name = "watchlist/partials/watchlist_acknowledge.html"

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        """modal confirmation to acknowledge watch list"""
        self.watchlist = self.get_object(kwargs["pk"])
        context = {"watchlist": self.watchlist}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """acknowledge watch list"""
        try:
            self.watchlist = self.get_object(kwargs["pk"])
            self.watchlist.acknowledged = timezone.now()
            self.watchlist.acknowledged_by = request.user
            self.watchlist.save()
            if next_url := self.request.POST.get("next") or self.request.GET.get("next"):
                return redirect(next_url)
            else:
                return redirect("/")

        except Exception as err:
            logging.error(err)
            return HttpResponse(500)
