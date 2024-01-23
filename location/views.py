"""Location CRUD views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import GenericSingleModelSearchView, ObjectDeleteHTMXView

from .forms import LocationForm
from .models import Location


class LocationSearchView(LoginRequiredMixin, GenericSingleModelSearchView):
    """View for searching for a Location."""

    model = Location
    query_name = "location_query"
    search_fields = ["name", "room__name", "description"]
    template_name = "location/location_search_results.html"


class LocationCreateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView):
    """Location create view."""

    model = Location
    form_class = LocationForm
    template_name = "location/location_create.html"
    success_url = reverse_lazy("location_list")


class LocationUpdateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView):
    """Location update view."""

    model = Location
    form_class = LocationForm
    template_name = "location/location_update.html"
    success_url = reverse_lazy("location_list")


class LocationDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Location delete view."""

    model = Location
    action_url = "location_delete"
    success_url = reverse_lazy("location_list")


class LocationDetailView(LoginRequiredMixin, DetailView):
    """Location detail view."""

    model = Location
    template_name = "location/location_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get items for pagination
        stock_entries = self.object.stock_entries.all().filter(remaining_quantity__gt=0).order_by("stock")
        # paginate items
        paginator = Paginator(stock_entries, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class LocationListView(LoginRequiredMixin, ListView):
    """Location list view."""

    model = Location
    context_object_name = "locations"
    template_name = "location/location_list.html"
    paginate_by = 5
