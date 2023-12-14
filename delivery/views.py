"""Delivery views."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from core.mixins import SuccessUrlMixin

from .models import Delivery
from .forms import DeliveryForm


class DeliveryCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """View for creating a Delivery."""

    model = Delivery
    template_name = "delivery/delivery_create.html"
    form_class = DeliveryForm
    success_url = reverse_lazy("delivery_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Delivery successfully created.")
        return response


class DeliveryDeleteView(LoginRequiredMixin, View):
    """View for deleting a Delivery."""

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning a Delivery delete form."""
        delivery = Delivery.objects.get(pk=kwargs["pk"])
        return render(
            request, "delivery/delivery_delete_form.html", {"delivery": delivery}
        )

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting a Delivery."""
        delivery = Delivery.objects.get(pk=kwargs["pk"])
        delivery.delete()
        messages.success(request, "Delivery deleted successfully.")
        return redirect("delivery_list")


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


class DeliveryUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """View for updating a Delivery."""

    model = Delivery
    form_class = DeliveryForm
    template_name = "delivery/delivery_update.html"
    success_url = reverse_lazy("delivery_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Delivery successfully updated.")
        return response
