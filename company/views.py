"""Views for the company app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import SuccessUrlMixin, FormValidMessageMixin
from core.views.generic import ObjectDeleteHTMXView

from .models import Company
from .forms import CompanyForm


# company search view
@login_required
def company_search(request):
    """HTMX GET request for returning a list of search companies"""
    query = ""
    company_type = ""
    if "manufacturer_query" in request.GET:
        query = request.GET.get("manufacturer_query", "")
        company_type = "manufacturer"
    elif "supplier_query" in request.GET:
        query = request.GET.get("supplier_query", "")
        company_type = "supplier"
    if query:
        queries = [
            Q(name__icontains=term) | Q(description__icontains=term)
            for term in query.split()
        ]
        query = queries.pop()
        for company in queries:
            query &= company
        companies = Company.objects.filter(query)[:5]
    else:
        companies = []
    return render(
        request,
        "company/company_search_results.html",
        {"found_companies": companies, "company_type": company_type},
    )


class CompanyCreateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView
):
    """View for creating a Company."""

    model = Company
    form_class = CompanyForm
    template_name = "company/company_create.html"
    success_url = reverse_lazy("company_list")


class CompanyUpdateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView
):
    """View for updating a Company."""

    model = Company
    form_class = CompanyForm
    template_name = "company/company_update.html"
    success_url = reverse_lazy("company_list")


class CompanyDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """View for deleting a Company."""

    model = Company
    action_url = "company_delete"
    success_url = reverse_lazy("company_list")


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """View for displaying a Company."""

    model = Company
    template_name = "company/company_detail.html"


class CompanyListView(LoginRequiredMixin, ListView):
    """View for displaying a list of Companies."""

    model = Company
    context_object_name = "companies"
    template_name = "company/company_list.html"
    paginate_by = 15
