""" views for watchlist """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from item.models import WatchList


class WatchListView(LoginRequiredMixin, ListView):
    """Watch list view."""

    template_name = "watchlist/watchlist_list.html"
    context_object_name = "watchlists"

    def get_queryset(self):
        """Return all watchlists."""
        return WatchList.objects.filter(is_active=True, notification=True)
