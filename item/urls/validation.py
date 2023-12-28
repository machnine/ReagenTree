"""validation urls"""
from django.urls import path

1
from item.views import (
    ValidationCreateView,
    ValidationDetailView,
    ValidationUpdateView,
    ValidationDeleteView,
)


urlpatterns = [
    path(
        "<str:object_type>/<int:object_id>/create/",
        ValidationCreateView.as_view(),
        name="validation_create",
    ),
    path("<int:pk>/update/", ValidationUpdateView.as_view(), name="validation_update"),
    path(
        "<str:object_type>/<int:object_id>/detail/",
        ValidationDetailView.as_view(),
        name="validation_detail",
    ),
    path("<int:pk>/delete/", ValidationDeleteView.as_view(), name="validation_delete"),
]
