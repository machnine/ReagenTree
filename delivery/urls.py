"""Delivery URLs"""
from django.urls import path

from .views import (
    DeliveryCreateView,
    DeliveryDeleteView,
    DeliveryDetailView,
    DeliveryListView,
    DeliveryUpdateView,
)

urlpatterns = [
    path("", DeliveryListView.as_view(), name="delivery_list"),
    path("create/", DeliveryCreateView.as_view(), name="delivery_create"),
    path("<int:pk>/", DeliveryDetailView.as_view(), name="delivery_detail"),
    path("<int:pk>/update/", DeliveryUpdateView.as_view(), name="delivery_update"),
    path("<int:pk>/delete/", DeliveryDeleteView.as_view(), name="delivery_delete"),
]
