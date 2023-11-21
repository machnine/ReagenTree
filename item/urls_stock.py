"""StockItem Urls"""
from django.urls import path

from .views import StockItemCreateView, StockItemListView

urlpatterns = [
    path("create/", StockItemCreateView.as_view(), name="stock_create"),
    path("", StockItemListView.as_view(), name="stock_list"),
]
