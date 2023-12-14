"""Location CRUD views."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from core.mixins import SuccessUrlMixin

from .models import Location

form_fields = ["name", "room", "description"]


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


class LocationCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Location create view."""

    model = Location
    fields = form_fields
    template_name = "location/location_create.html"
    success_url = reverse_lazy("location_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Location { form.instance.name } created successfully."
        )
        return response


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
        messages.success(request, f"Location { location.name } deleted successfully.")
        return redirect("location_list")


class LocationDetailView(LoginRequiredMixin, DetailView):
    """Location detail view."""

    model = Location
    template_name = "location/location_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get items for pagination
        stockitems = self.object.stockitems.all()
        # paginate items
        paginator = Paginator(stockitems, self.paginate_by)
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


class LocationUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """Location update view."""

    model = Location
    fields = form_fields
    template_name = "location/location_update.html"
    success_url = reverse_lazy("location_list")

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Location { form.instance.name } updated successfully."
        )
        return response
