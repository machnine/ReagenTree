"""Delivery URLs"""
from django.urls import path

from .views import (
    DeliveryCreateView,
    DeliveryDeleteView,
    DeliveryDetailView,
    DeliveryListView,
    DeliveryUpdateView,
    DeliveryAttachmentUploadView,
    DeliveryAttachmentDeleteView,
    DeliveryAttachmentUpdateView,
)

urlpatterns = [
    path("", DeliveryListView.as_view(), name="delivery_list"),
    path("create/", DeliveryCreateView.as_view(), name="delivery_create"),
    path("<int:pk>/", DeliveryDetailView.as_view(), name="delivery_detail"),
    path("<int:pk>/update/", DeliveryUpdateView.as_view(), name="delivery_update"),
    path("<int:pk>/delete/", DeliveryDeleteView.as_view(), name="delivery_delete"),
    path(
        "<int:pk>/attachment/upload/",
        DeliveryAttachmentUploadView.as_view(),
        name="delivery_attachment_upload",
    ),
    path(
        "attachment/<int:pk>/update/",
        DeliveryAttachmentUpdateView.as_view(),
        name="delivery_attachment_update",
    ),
    path(
        "attachment/<int:pk>/delete/",
        DeliveryAttachmentDeleteView.as_view(),
        name="delivery_attachment_delete",
    ),
]
