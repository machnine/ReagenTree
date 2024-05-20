"""Views for the company app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView

from .forms import CompanyForm
from .models import Company


class CompanySearchView(LoginRequiredMixin, ListView):
    """View for searching for a Company same logic as core.views.search.GenericSingleModelSearchView"""

    model = Company
    template_name = "company/company_search_results.html"
    search_fields = ["name", "description"]
    extra_filters = {}
    context_object_name = "search_results"
    context_object_limit = 5

    def get_queryset(self):
        query = ""
        if "manufacturer_query" in self.request.GET:
            query = self.request.GET.get("manufacturer_query", "")
        elif "supplier_query" in self.request.GET:
            query = self.request.GET.get("supplier_query", "")

        if not query:
            return self.model.objects.none()

        terms = query.split()
        base_query = Q()

        for term in terms:
            term_query = Q(**{f"{self.search_fields[0]}__icontains": term})
            for field in self.search_fields[1:]:
                term_query |= Q(**{f"{field}__icontains": term})
            base_query &= term_query  # Combine with the base query using AND
        return self.model.objects.filter(base_query, **self.extra_filters).distinct()[: self.context_object_limit]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_type = ""
        if "manufacturer_query" in self.request.GET:
            company_type = "manufacturer"
        elif "supplier_query" in self.request.GET:
            company_type = "supplier"

        context["company_type"] = company_type
        context["query"] = self.request.GET.get("manufacturer_query") or self.request.GET.get("supplier_query", "")
        return context


class CompanyCreateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView):
    """View for creating a Company."""

    model = Company
    form_class = CompanyForm
    template_name = "company/company_create.html"
    success_url = reverse_lazy("company_list")


class CompanyUpdateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView):
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

    def get_queryset(self):
        query_set = super().get_queryset()
        sort_by = self.request.GET.get("sort_by", "name")
        order = self.request.GET.get("order", "asc")
        if order == "desc":
            sort_by = f"-{sort_by}"
        return query_set.order_by(sort_by)
