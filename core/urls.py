"""
URL configuration for the whole project.
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from user import urls as user_urls
from company import urls as company_urls

from .views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("", include(user_urls)),
    path("company/", include(company_urls)),
]
