"""Stock Urls"""
from django.urls import path

from item.views import (
    StockCreateView,
    StockListView,
    StockDeleteView,
    StockUpdateView,
    StockEntryDeleteView,
    StockEntryUpdateView,
)

urlpatterns = [
    path("", StockListView.as_view(), name="stock_list"),
    path("create/", StockCreateView.as_view(), name="stock_create"),
    path("<int:pk>/delete/", StockDeleteView.as_view(), name="stock_delete"),
    path("<int:pk>/update/", StockUpdateView.as_view(), name="stock_update"),
    path(
        "entry/<int:pk>/delete/",
        StockEntryDeleteView.as_view(),
        name="stock_entry_delete",
    ),
    path(
        "entry/<int:pk>/update/",
        StockEntryUpdateView.as_view(),
        name="stock_entry_update",
    ),
]
