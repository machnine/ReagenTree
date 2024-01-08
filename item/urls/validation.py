"""validation urls"""
from django.urls import path
from item.views import ValidationUpdateView, ValidationAuthorisationHtmxView

urlpatterns = [
    path("<int:pk>/update/", ValidationUpdateView.as_view(), name="validation_update"),
    path(
        "<int:pk>/authorise/",
        ValidationAuthorisationHtmxView.as_view(),
        name="validation_authorise",
    ),
]
