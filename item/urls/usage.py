"""Usage Urls"""
from django.urls import path

from item.views import UsageUpdateHtmxView

urlpatterns = [
    path("<int:pk>/update/", UsageUpdateHtmxView.as_view(), name="usage_update")
]
