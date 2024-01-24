"""watchlist URL Configuration"""
from django.urls import path

from item.views import WatchListCreateView, WatchListDeleteView, WatchListView

urlpatterns = [
    path("", WatchListView.as_view(), name="watchlist"),
    path("create/", WatchListCreateView.as_view(), name="watchlist_create"),
    path("delete/<int:pk>/", WatchListDeleteView.as_view(), name="watchlist_delete"),
]
