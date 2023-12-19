"""Stock Urls"""
from django.urls import path

from item.views import (
    StockCreateView,
    StockListView,
    StockDetailView,
    StockDeleteView,
    StockUpdateView,
)

urlpatterns = [
    path("", StockListView.as_view(), name="stock_list"),
    path("create/", StockCreateView.as_view(), name="stock_create"),
    path("<int:pk>/delete/", StockDeleteView.as_view(), name="stock_delete"),
    path("<int:pk>/", StockDetailView.as_view(), name="stock_detail"),
    path("<int:pk>/update/", StockUpdateView.as_view(), name="stock_update"),
]
