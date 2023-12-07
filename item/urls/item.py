"""Item Urls"""
from django.urls import path

from item.views import (
    ItemCreateView,
    ItemDeleteView,
    ItemDetailView,
    ItemListView,
    ItemUpdateView,
    item_search,
)

urlpatterns = [
    path("create/", ItemCreateView.as_view(), name="item_create"),
    path("<int:pk>/delete/", ItemDeleteView.as_view(), name="item_delete"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("", ItemListView.as_view(), name="item_list"),
    path("<int:pk>/update/", ItemUpdateView.as_view(), name="item_update"),
    path("search/", item_search, name="item_search"),
]
