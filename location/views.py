"""Location CRUD views."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import SuccessUrlMixin, FormValidMessageMixin
from core.views.generic import ObjectDeleteHTMXView

from .models import Location
from .forms import LocationForm


# Location search view
@login_required
def location_search(request):
    """HTMX GET request for returning a list of search locations"""
    query = request.GET.get("location_query", "")
    if query:
        queries = [Q(name__icontains=term) for term in query.split()]
        query = queries.pop()
        for location in queries:
            query &= location
        locations = Location.objects.filter(query)[:5]
    else:
        locations = []
    return render(
        request,
        "location/location_search_results.html",
        {"found_locations": locations},
    )


class LocationCreateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView
):
    """Location create view."""

    model = Location
    is_created = True
    form_class = LocationForm
    template_name = "location/location_create.html"
    success_url = reverse_lazy("location_list")



class LocationUpdateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView
):
    """Location update view."""

    model = Location
    is_updated = True
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
        stocks = self.object.stocks.all()
        # paginate items
        paginator = Paginator(stocks, self.paginate_by)
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
