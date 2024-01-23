"""watchlist URL Configuration"""
from django.urls import path

from item.views import WatchListView

urlpatterns = [
    path("", WatchListView.as_view(), name="watchlist"),
]
