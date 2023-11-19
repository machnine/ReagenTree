"""Location CRUD views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .models import Location


class LocationCreateView(LoginRequiredMixin, CreateView):
    """Location create view."""

    model = Location
    fields = ["name", "description"]
    template_name = "location/location_create.html"
    success_url = reverse_lazy("location_list")


class LocationDeleteView(LoginRequiredMixin, View):
    """Location delete view."""

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning a Location delete form."""
        location = Location.objects.get(pk=kwargs["pk"])
        return render(
            request, "location/location_delete_form.html", {"location": location}
        )

    def post(self, request, *args, **kwargs):
        """Handle POST request."""
        location = Location.objects.get(pk=kwargs["pk"])
        location.delete()
        return redirect("location_list")


class LocationDetailView(LoginRequiredMixin, DetailView):
    """Location detail view."""

    model = Location
    template_name = "location/location_detail.html"


class LocationListView(LoginRequiredMixin, ListView):
    """Location list view."""

    model = Location
    context_object_name = "locations"
    template_name = "location/location_list.html"


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    """Location update view."""

    model = Location
    fields = ["name", "description"]
    template_name = "location/location_update.html"
    success_url = reverse_lazy("location_list")
