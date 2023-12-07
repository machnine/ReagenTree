"""StockItem Urls"""
from django.urls import path

from item.views import (
    StockItemCreateView,
    StockItemListView,
    StockItemDetailView,
    StockItemDeleteView,
)

urlpatterns = [
    path("", StockItemListView.as_view(), name="stock_list"),
    path("create/", StockItemCreateView.as_view(), name="stock_create"),
    path("<int:pk>/delete/", StockItemDeleteView.as_view(), name="stock_delete"),
    path("<int:pk>/", StockItemDetailView.as_view(), name="stock_detail"),
]
