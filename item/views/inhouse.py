"""In house reagent views """
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.views.generic import ObjectDeleteHTMXView
from item.forms import InhouseReagentForm, ReagentComponentForm
from item.models import InhouseReagent, ReagentComponent


# mixins
class InhouseReagentFormProccessorMixin:
    """Mixin for processing inhouse reagent form"""

    def get_success_url(self):
        """return the URL to redirect to, after processing a valid form."""

        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return super().get_success_url()

    def get_formset(self, data=None, instance=None, extra_forms=1):
        """Helper function to get formset"""
        ReagentComponentFormSet = inlineformset_factory(
            InhouseReagent,
            ReagentComponent,
            form=ReagentComponentForm,
            extra=extra_forms,
        )
        return ReagentComponentFormSet(data=data, instance=instance)

    def form_valid(self, form, formset):
        """form valid method"""
        # Validate that at least one ReagentComponent is present
        if not formset.forms or all(
            form.cleaned_data.get("DELETE", False) for form in formset.forms if form.cleaned_data
        ):
            messages.error(self.request, "At least one component is required.")
            return self.form_invalid(form, formset)
        action = "updated"
        # Set the created_by and last_updated_by fields
        if not bool(form.instance.pk):
            action = "created"
            form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        # Save the main form (InhouseReagent)
        self.object = form.save()
        # Set the instance for the formset and save it
        formset.instance = self.object
        formset.save()
        # Messages

        action_success = mark_safe(f"{self.model.__name__}: <i><b>{form.instance}</b></i> {action} successfully.")
        messages.success(self.request, action_success)
        # Now call the superclass's form_valid method
        return super().form_valid(form)

    def form_invalid(self, form, formset):
        """form invalid method"""
        form_context = {"form": form, "formset": formset}
        return render(self.request, self.template_name, form_context)


# inhouse reagent search view
@login_required
def inhouse_reagent_search(request):
    """HTMX view for returning a list of inhouse reagents"""
    query = request.GET.get("inhouse_query", "")
    if query:
        queries = [Q(name__icontains=term) | Q(description__icontains=term) for term in query.split()]
        query = queries.pop()
        for reagent in queries:
            query &= reagent
        inhouse_reagents = InhouseReagent.objects.filter(query)[:5]
    else:
        inhouse_reagents = []
    return render(request, "inhouse/partials/search_results.html", {"found_inhouse_reagents": inhouse_reagents})


# CRUD views
class InhouseReagentCreateView(LoginRequiredMixin, InhouseReagentFormProccessorMixin, CreateView):
    """Create view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_create.html"
    form_class = InhouseReagentForm
    success_url = reverse_lazy("inhouse_list")

    def get(self, request, *args, **kwargs):
        """Override get to set initial form data"""
        form = self.get_form()

        # Formset for reagent components
        formset = self.get_formset(instance=InhouseReagent())
        form_context = {"form": form, "formset": formset}
        return render(request, self.template_name, form_context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset(data=request.POST, instance=InhouseReagent())
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)


class InhouseReagentUpdateView(LoginRequiredMixin, InhouseReagentFormProccessorMixin, UpdateView):
    """Update view for inhouse reagents"""

    model = InhouseReagent
    template_name = "inhouse/inhouse_update.html"
    form_class = InhouseReagentForm
    success_url = reverse_lazy("inhouse_list")

    def get(self, request, *args, **kwargs):
        """Override get to set initial form data"""
        self.object = self.get_object()
        form = self.get_form()

        # Formset for reagent components
        formset = self.get_formset(instance=self.object)
        form_context = {"form": form, "formset": formset}
        return render(request, self.template_name, form_context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset(data=request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)


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
