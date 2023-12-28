"""Stock validation views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from core.mixins import SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView
from item.models import ReagentValidation
from item.forms import ValidationForm


class ValidationCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create validation view"""

    model = ReagentValidation
    form_class = ValidationForm
    template_name = "validation/validation_create.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        """Get the object to validate based on the object_type and object_id from the URL."""
        try:
            content_type = ContentType.objects.get(model=self.kwargs["object_type"])
            self.object_to_validate = get_object_or_404(
                content_type.model_class(), pk=self.kwargs["object_id"]
            )
        except (ObjectDoesNotExist, ValueError):
            return HttpResponseNotAllowed("Invalid object type or object ID")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_to_validate"] = self.object_to_validate
        return context

    def form_valid(self, form):
        # Set the content_object for the validation
        object_content_type = ContentType.objects.get_for_model(self.object_to_validate)
        form.instance.content_type = object_content_type
        form.instance.object_id = self.object_to_validate.id
        form.instance.validated_by = self.request.user
        return super().form_valid(form)


class ValidationUpdateView(LoginRequiredMixin, UpdateView):
    """Update validation view"""

    model = ReagentValidation
    form_class = ValidationForm
    template_name = "validation/validation_update.html"

    def form_valid(self, form):
        """Add user to form"""
        form.instance.validated_by = self.request.user
        return super().form_valid(form)


class ValidationDetailView(LoginRequiredMixin, ListView):
    """Detail validation view"""

    model = ReagentValidation
    template_name = "validation/validation_detail.html"
    context_object_name = "validations"

    def get_queryset(self):
        """Get the validation objects for the object_type and object_id from the URL."""
        content_object_type = get_object_or_404(
            ContentType, model=self.kwargs["object_type"]
        )
        return ReagentValidation.objects.filter(
            content_type=content_object_type, object_id=self.kwargs["object_id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        object_type = self.kwargs["object_type"]
        object_to_validate = queryset.first().content_object
        object_to_validate_detail_url = f"{object_type}_detail"
        context.update(
            {
                "object_type": object_type,
                "object_to_validate": object_to_validate,
                "object_to_validate_detail_url": object_to_validate_detail_url,
            }
        )

        return context


class ValidationDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete validation view"""

    model = ReagentValidation
    action_url = "validation_delete"
    success_url = reverse_lazy("validation_list")
