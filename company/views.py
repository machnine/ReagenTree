"""Views for the company app."""
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

from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """View for creating a Company."""

    model = Company
    fields = ["name", "description"]
    template_name = "company/company_create.html"
    success_url = reverse_lazy("company_list")

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        return super().form_valid(form)


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


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating a Company."""

    model = Company
    fields = ["name", "description"]
    template_name = "company/company_update.html"
    success_url = reverse_lazy("company_list")

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        return super().form_valid(form)
