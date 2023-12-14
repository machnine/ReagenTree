"""Item Urls"""
from django.urls import path

from item.views import (
    item_search,
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
    ItemAttachmentUploadView,
    ItemAttachmentDeleteView,
    ItemAttachmentUpdateView,
)

urlpatterns = [
    path("create/", ItemCreateView.as_view(), name="item_create"),
    path("<int:pk>/delete/", ItemDeleteView.as_view(), name="item_delete"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("", ItemListView.as_view(), name="item_list"),
    path("<int:pk>/update/", ItemUpdateView.as_view(), name="item_update"),
    path("search/", item_search, name="item_search"),
    path(
        "<int:pk>/attachment/upload/",
        ItemAttachmentUploadView.as_view(),
        name="item_attachment_upload",
    ),
    path(
        "attachment/<int:pk>/delete/",
        ItemAttachmentDeleteView.as_view(),
        name="item_attachment_delete",
    ),
    path(
        "attachment/<int:pk>/update/",
        ItemAttachmentUpdateView.as_view(),
        name="item_attachment_update",
    ),
]
