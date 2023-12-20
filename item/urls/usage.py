"""Usage Urls"""
from django.urls import path

from item.views import UsageCreateView

urlpatterns = [
    path("stock/<int:pk>/", UsageCreateView.as_view(), name="usage_create"),
]
