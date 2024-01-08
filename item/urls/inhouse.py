""" URL paths for inhouse reagents"""
from django.urls import path
from item.views import (
    InhouseReagentListView,
    InhouseReagentDetailView,
    InhouseReagentCreateView,
    InhouseReagentUpdateView,
    InhouseReagentDeleteView,
    InhouseValidationListView,
)

urlpatterns = [
    path("", InhouseReagentListView.as_view(), name="inhouse_list"),
    path("<int:pk>/", InhouseReagentDetailView.as_view(), name="inhouse_detail"),
    path("create/", InhouseReagentCreateView.as_view(), name="inhouse_create"),
    path("<int:pk>/update/", InhouseReagentUpdateView.as_view(), name="inhouse_update"),
    path("<int:pk>/delete/", InhouseReagentDeleteView.as_view(), name="inhouse_delete"),
    path(
        "validations/",
        InhouseValidationListView.as_view(),
        name="inhouse_validation_list",
    ),
]
