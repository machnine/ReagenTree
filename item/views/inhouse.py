"""In house reagent views """
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from item.models import InhouseReagent, ReagentComponent


class InhouseReagentListView(LoginRequiredMixin, ListView):
    """List view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_list.html"
    context_object_name = "inhouse_reagents"


class InhouseReagentDetailView(LoginRequiredMixin, DetailView):
    """Detail view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_detail.html"
    context_object_name = "inhouse_reagent"


class InhouseReagentCreateView(LoginRequiredMixin, CreateView):
    """Create view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_create.html"
    fields = ["name", "description", "components"]
    success_url = reverse_lazy("inhouse_list")

    def form_valid(self, form):
        """Override form_valid to set created_by and last_updated_by"""
        form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)


class InhouseReagentUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_update.html"
    fields = ["name", "description", "components"]
    success_url = reverse_lazy("inhouse_list")

    def form_valid(self, form):
        """Override form_valid to set last_updated_by"""
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)
