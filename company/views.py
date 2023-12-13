"""Views for the company app."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from core.mixins import SuccessUrlMixin

from .models import Company


class CompanyCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """View for creating a Company."""

    model = Company
    fields = ["name", "description", "website", "phone"]
    template_name = "company/company_create.html"
    success_url = reverse_lazy("company_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Company { form.instance.name } created successfully."
        )
        return response


class CompanyDeleteView(LoginRequiredMixin, View):
    """View for deleting a Company."""

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning a Company delete form."""
        company = Company.objects.get(pk=kwargs["pk"])
        return render(request, "company/company_delete_form.html", {"company": company})

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting a Company."""
        company = Company.objects.get(pk=kwargs["pk"])
        company.delete()
        messages.success(request, f"Company { company.name } deleted successfully.")
        return redirect("company_list")


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


class CompanyUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """View for updating a Company."""

    model = Company
    fields = ["name", "description", "website", "phone"]
    template_name = "company/company_update.html"
    success_url = reverse_lazy("company_list")

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Company { form.instance.name } updated successfully."
        )
        return response
