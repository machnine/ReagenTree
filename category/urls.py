"""Category URL Configuration"""
from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
    category_search,
)

urlpatterns = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("create/", CategoryCreateView.as_view(), name="category_create"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("<int:pk>/update/", CategoryUpdateView.as_view(), name="category_update"),
    path("<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
    path("search/", category_search, name="category_search"),
]
