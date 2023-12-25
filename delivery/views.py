"""Delivery views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView

from attachment.views import (
    AttachmentDeleteView,
    AttachmentUpdateView,
    AttachmentUploadView,
)

from .models import Delivery, DeliveryAttachment
from .forms import (
    DeliveryForm,
    DeliveryAttachmentCreateForm,
    DeliveryAttachmentUpdateForm,
)


class DeliveryCreateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView
):
    """View for creating a Delivery."""

    model = Delivery
    is_created = True
    form_class = DeliveryForm
    success_url = reverse_lazy("delivery_list")
    template_name = "delivery/delivery_create.html"


class DeliveryDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """View for deleting a Delivery."""

    model = Delivery
    action_url = "delivery_delete"
    success_url = reverse_lazy("delivery_list")


class DeliveryDetailView(LoginRequiredMixin, DetailView):
    """View for displaying a Delivery."""

    model = Delivery
    template_name = "delivery/delivery_detail.html"

    def get_context_data(self, **kwargs):
        """Add related stocks to context."""
        context = super().get_context_data(**kwargs)
        stocks = {s.item: [] for s in self.object.stocks.all()}
        for stock in self.object.stocks.all():
            stocks[stock.item].append(stock)
        context["stocks"] = stocks
        context["attachments"] = DeliveryAttachment.objects.filter(
            object_id=self.object.id
        )
        return context


class DeliveryListView(LoginRequiredMixin, ListView):
    """View for displaying a list of Deliveries."""

    model = Delivery
    context_object_name = "deliveries"
    template_name = "delivery/delivery_list.html"
    paginate_by = 10


class DeliveryUpdateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView
):
    """View for updating a Delivery."""

    model = Delivery
    is_updated = True
    form_class = DeliveryForm
    success_url = reverse_lazy("delivery_list")
    template_name = "delivery/delivery_update.html"


#
# Delivery attachment CRUD views
#
class DeliveryAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for DeliveryAttachment model"""

    owner_model = Delivery
    form_class = DeliveryAttachmentCreateForm
    success_url_name = "delivery_detail"
    template_name = "attachment/attachment_upload_form.html"
    upload_url_name = "delivery_attachment_upload"


class DeliveryAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for DeliveryAttachment model"""

    model = DeliveryAttachment
    template_name = "delivery/delivery_detail_attachment_delete.html"
    success_url_name = "delivery_detail"


class DeliveryAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for DeliveryAttachment model"""

    owner_model = Delivery
    model = DeliveryAttachment
    form_class = DeliveryAttachmentUpdateForm
    template_name = "delivery/delivery_detail_attachment_update.html"
    success_url_name = "delivery_detail"
