"""Stock Urls"""
from django.urls import path

from item.views import (
    StockAttachmentDeleteView,
    StockAttachmentUpdateView,
    StockAttachmentUploadView,
    StockCreateView,
    StockDeleteView,
    StockDetailView,
    StockEntryDeleteView,
    StockEntryUpdateView,
    StockLabelPrintView,
    StockListView,
    StockUpdateView,
    StockValidationCreateView,
    StockValidationDeleteView,
    StockValidationListView,
)

urlpatterns = [
    path("", StockListView.as_view(), name="stock_list"),
    path("create/", StockCreateView.as_view(), name="stock_create"),
    path("<int:pk>/delete/", StockDeleteView.as_view(), name="stock_delete"),
    path("<int:pk>/update/", StockUpdateView.as_view(), name="stock_update"),
    path("<int:pk>/", StockDetailView.as_view(), name="stock_detail"),
    path("<int:pk>/attachment/upload/", StockAttachmentUploadView.as_view(), name="stock_attachment_upload"),
    path("attachment/<int:pk>/update/", StockAttachmentUpdateView.as_view(), name="stock_attachment_update"),
    path("attachment/<int:pk>/delete/", StockAttachmentDeleteView.as_view(), name="stock_attachment_delete"),
    path("entry/<int:pk>/delete/", StockEntryDeleteView.as_view(), name="stock_entry_delete"),
    path("entry/<int:pk>/update/", StockEntryUpdateView.as_view(), name="stock_entry_update"),
    path("<int:pk>/validation/create/", StockValidationCreateView.as_view(), name="stock_validation_create"),
    path("validation/<int:pk>/delete/", StockValidationDeleteView.as_view(), name="stock_validation_delete"),
    path("validations/", StockValidationListView.as_view(), name="stock_validation_list"),
    path("<int:pk>/print/", StockLabelPrintView.as_view(), name="stock_label_print"),
]
