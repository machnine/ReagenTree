""" URL paths for inhouse reagents"""
from django.urls import path

from item.views import (
    InhouseReagentCreateView,
    InhouseReagentDeleteView,
    InhouseReagentDetailView,
    InhouseReagentListView,
    InhouseReagentUpdateView,
    ReagentComponentCreateView,
    ReagentComponentDeleteView,
    ReagentComponentUpdateView,
    inhouse_reagent_search,
)

urlpatterns = [
    path("", InhouseReagentListView.as_view(), name="inhouse_list"),
    path("<int:pk>/", InhouseReagentDetailView.as_view(), name="inhouse_detail"),
    path("create/", InhouseReagentCreateView.as_view(), name="inhouse_create"),
    path("<int:pk>/update/", InhouseReagentUpdateView.as_view(), name="inhouse_update"),
    path("<int:pk>/component/update/", ReagentComponentUpdateView.as_view(), name="component_update"),
    path("<int:pk>/delete/", InhouseReagentDeleteView.as_view(), name="inhouse_delete"),
    path("search/", inhouse_reagent_search, name="inhouse_search"),
    path("<int:reagent_pk>/component/create/", ReagentComponentCreateView.as_view(), name="component_create"),
    path("component/<int:pk>/delete/", ReagentComponentDeleteView.as_view(), name="component_delete"),

]
