"""StockItem Urls"""
from django.urls import path

from item.views import StockItemCreateView, StockItemListView, StockItemDetailView

urlpatterns = [
    path("create/", StockItemCreateView.as_view(), name="stock_create"),
    path("", StockItemListView.as_view(), name="stock_list"),
    path("<int:pk>/", StockItemDetailView.as_view(), name="stock_detail"),
]
