"""In house reagent views """

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView
from item.forms import InhouseReagentForm, ReagentComponentForm
from item.models import InhouseReagent, ReagentComponent


# CRUD views
class InhouseReagentCreateView(LoginRequiredMixin, CreateView):
    """Create view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_create.html"
    form_class = InhouseReagentForm
    success_url = reverse_lazy("inhouse_list")


class InhouseReagentUpdateView(LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView):
    """Update view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_update.html"
    form_class = InhouseReagentForm
    success_url = reverse_lazy("inhouse_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.category:
            context["category_name"] = self.object.category.name
        return context


class InhouseReagentDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for inhouse reagent model"""

    model = InhouseReagent
    action_url = "inhouse_delete"
    success_url = reverse_lazy("inhouse_list")


class InhouseReagentListView(LoginRequiredMixin, ListView):
    """List view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_list.html"
    context_object_name = "inhouse_reagents"
    paginate_by = 16


class InhouseReagentDetailView(LoginRequiredMixin, DetailView):
    """Detail view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_detail.html"
    context_object_name = "inhouse_reagent"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reagent_components = ReagentComponent.objects.filter(reagent=self.object)
        context["reagent_components"] = reagent_components
        return context


class ReagentComponentCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for inhouse reagent components
    This handles the HTMX request from the inhouse detail view
    """

    model = ReagentComponent
    template_name = "inhouse/partials/component_form.html"
    form_class = ReagentComponentForm

    def dispatch(self, request, *args, **kwargs):
        # Retrieve and store the InhouseReagent instance for later use
        self.reagent = get_object_or_404(InhouseReagent, pk=kwargs.get("reagent_pk"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect to the detail view of the associated InhouseReagent
        return reverse_lazy("inhouse_detail", kwargs={"pk": self.reagent.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the InhouseReagent instance to the template context
        context["reagent"] = self.reagent
        return context

    def form_valid(self, form):
        # Associate the component with the retrieved InhouseReagent
        component = form.save(commit=False)

        # Check if the component's stock is already in the reagent's components
        if ReagentComponent.objects.filter(reagent=self.reagent, stock=component.stock).exists():
            messages.error(self.request, "This stock is already part of the reagent.")
            return HttpResponseRedirect(self.get_success_url())

        # Check if the stock's source is the reagent itself
        if component.stock.source == self.reagent:
            messages.error(self.request, "The stock's source cannot be the reagent itself.")
            return HttpResponseRedirect(self.get_success_url())

        component.reagent = self.reagent
        component.save()
        action_success = format_html(f"<i><b>{component.stock.source}</b></i> added successfully.")
        messages.success(self.request, action_success)
        return super().form_valid(form)


class ReagentComponentUpdateView(LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView):
    """Update view for inhouse reagent components"""

    model = ReagentComponent
    template_name = "inhouse/component_update.html"
    form_class = ReagentComponentForm
    success_url = reverse_lazy("inhouse_list")


class ReagentComponentDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for inhouse reagent components"""

    model = ReagentComponent
    action_url = "component_delete"
    success_url = None

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an object."""
        with transaction.atomic():
            obj = self.get_object(kwargs["pk"])
            reagent_id = obj.reagent.pk
            obj.delete()
            messages.success(request, "Component deleted successfully.")
        if not request.POST.get("next"):
            self.success_url = reverse_lazy("inhouse_detail", kwargs={"pk": reagent_id})
        return redirect(self.get_success_url())
