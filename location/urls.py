"""Location URLS"""
from django.urls import path

from .views import (
    LocationCreateView,
    LocationDeleteView,
    LocationDetailView,
    LocationListView,
    LocationSearchView,
    LocationUpdateView,
)

urlpatterns = [
    path("", LocationListView.as_view(), name="location_list"),
    path("<int:pk>/", LocationDetailView.as_view(), name="location_detail"),
    path("create/", LocationCreateView.as_view(), name="location_create"),
    path("<int:pk>/update/", LocationUpdateView.as_view(), name="location_update"),
    path("<int:pk>/delete/", LocationDeleteView.as_view(), name="location_delete"),
    path("search/", LocationSearchView.as_view(), name="location_search"),
]
