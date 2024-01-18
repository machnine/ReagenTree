"""Usage Urls"""
from django.urls import path

from item.views import UsageQRUpdateView, UsageUpdateHtmxView

urlpatterns = [
    path("<int:pk>/htmx/update/", UsageUpdateHtmxView.as_view(), name="usage_htmx_update"),
    path("<int:pk>/qr/update/", UsageQRUpdateView.as_view(), name="usage_qr_update"),
]
