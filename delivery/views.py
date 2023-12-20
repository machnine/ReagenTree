"""Delivery views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView

from .models import Delivery
from .forms import DeliveryForm


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

