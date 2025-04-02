from django.urls import path

from .views import (
    NoticeArchiveView,
    NoticeCreateView,
    NoticeDetailView,
    NoticeListView,
    NoticeUpdateView,
)

urlpatterns = [
    path("", NoticeListView.as_view(), name="notice_list"),
    path("<int:pk>/", NoticeDetailView.as_view(), name="notice_detail"),
    path("create/", NoticeCreateView.as_view(), name="notice_create"),
    path("<int:pk>/update/", NoticeUpdateView.as_view(), name="notice_update"),
    path("<int:pk>/archive/", NoticeArchiveView.as_view(), name="notice_archive"),
]
