""" Company URLs"""
from django.urls import path

from .views import (
    company_search,
    CompanyCreateView,
    CompanyDeleteView,
    CompanyDetailView,
    CompanyListView,
    CompanyUpdateView,
)

urlpatterns = [
    path("", CompanyListView.as_view(), name="company_list"),
    path("create/", CompanyCreateView.as_view(), name="company_create"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),
    path("<int:pk>/update/", CompanyUpdateView.as_view(), name="company_update"),
    path("<int:pk>/delete/", CompanyDeleteView.as_view(), name="company_delete"),
    path("search/", company_search, name="company_search"),
]