"""Stock validation views"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView
from item.forms import ValidationForm
from item.models import InhouseReagentValidation, ReagentValidation, Stock, StockValidation


class ValidationUpdateView(LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView):
    """Generic validation update view"""

    model = ReagentValidation
    form_class = ValidationForm
    template_name = "validation/validation_update.html"
    success_url = reverse_lazy("stock_list")


class ValidationAuthorisationHtmxView(LoginRequiredMixin, SuccessUrlMixin, FormView):
    """HTMX view for authorising a validation"""

    template_name = "validation/validation_authorisation_form.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        """Check user permissions"""
        if not request.user.is_supervisor:
            messages.error(request, "You do not have permission to authorise validations.")
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_validation(self, pk):
        """Get validation object"""
        return get_object_or_404(ReagentValidation, pk=pk)

    def get(self, request, **kwargs):
        """HTMX GET request for authorising a validation"""
        validation = self.get_validation(kwargs["pk"])
        action_url = reverse_lazy("validation_authorise", kwargs={"pk": validation.pk})
        context = {"validation": validation, "action_url": action_url}
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        """HTMX POST request for authorising a validation"""
        validation = self.get_validation(kwargs["pk"])
        validation.authorised_by = self.request.user
        validation.authorised = timezone.now()
        validation.save()
        messages.success(request, "Validation authorised successfully.")
        return redirect(self.get_success_url())


# Stock Validations
class StockValidationCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for StockValidation model"""

    model = ReagentValidation
    form_class = ValidationForm
    template_name = "validation/validation_create.html"
    success_url = reverse_lazy("stock_list")

    def form_valid(self, form):
        # create validation
        form.instance.created_by = self.request.user
        validation = form.save()
        # link validation to stock
        stock_id = self.kwargs.get("pk")
        stock = get_object_or_404(Stock, pk=stock_id)
        StockValidation.objects.create(stock=stock, validation=validation)
        return HttpResponseRedirect(self.get_success_url())


class StockValidationDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete StockValidation (relation) and the associated Validation (object)"""

    model = StockValidation
    action_url = "stock_validation_delete"
    success_url = reverse_lazy("stock_detail")

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an object."""
        with transaction.atomic():
            obj = self.get_object(kwargs["pk"])
            stock_id = obj.stock.pk
            obj.validation.delete()
            messages.success(request, "Validation deleted successfully.")
        if not request.POST.get("next"):
            self.success_url = reverse_lazy("stock_detail", kwargs={"pk": stock_id})
        return redirect(self.get_success_url())


class StockValidationListView(LoginRequiredMixin, ListView):
    """List view for Stock with pending validations"""

    model = Stock
    context_object_name = "stocks"
    template_name = "validation/validation_list_stock.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(validations__isnull=True)
        return queryset.order_by("-delivery_date")


# Inhouse reagent validations
class InhouseValidationListView(LoginRequiredMixin, ListView):
    """List view for InhouseReagentValidation model"""

    model = InhouseReagentValidation
    context_object_name = "inhouse_reagents"
    template_name = "validation/validation_list_inhouse.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(validations__isnull=True)
        return queryset.order_by("-delivery_date")
