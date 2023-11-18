"""Location CRUD views."""
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .models import Location


class LocationCreateView(CreateView):
    """Location create view."""

    model = Location
    fields = ["name", "description"]
    template_name = "location/location_create.html"
    success_url = reverse_lazy("location_list")


class LocationDeleteView(View):
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


class LocationDetailView(DetailView):
    """Location detail view."""

    model = Location
    template_name = "location/location_detail.html"


class LocationListView(ListView):
    """Location list view."""

    model = Location
    context_object_name = "locations"
    template_name = "location/location_list.html"


class LocationUpdateView(UpdateView):
    """Location update view."""

    model = Location
    fields = ["name", "description"]
    template_name = "location/location_update.html"
    success_url = reverse_lazy("location_list")
