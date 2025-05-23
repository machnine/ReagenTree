"""Stock Item views"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView
from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView
from item.forms import StockEntryFormSet, StockEntryUpdateForm, StockForm
from item.forms.stock import StockAttachmentCreateForm, StockAttachmentUpdateForm
from item.models import Stock, StockAttachment, StockEntry
from label.views import LabelPrintBaseView


# Stock model CRUD views
class StockCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for Stock model"""

    model = Stock
    form_class = StockForm
    template_name = "stock/stock_create.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = StockEntryFormSet(self.request.POST) if self.request.POST else StockEntryFormSet()
        context["object_class"] = "stock"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        entries = context["entries"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            form.instance.last_updated_by = self.request.user
            self.object = form.save()  # Save Stock instance first
            # Get the quantity of entries from the form
            quantity = form.cleaned_data["quantity"]
            entries.instance = self.object  # Set the instance of the formset

            if entries.is_valid():
                location = entries.cleaned_data[0]["location"]
                for n in range(quantity):
                    # Create the StockEntry instances
                    entry = StockEntry(
                        location=location, stock=self.object, last_updated_by=self.request.user, ordinal_number=n + 1
                    )
                    entry.save()
                messages.success(self.request, "Stock created successfully")
                # check if the stock source is an Item, remind the user to check the product documentation
                if self.object.item:
                    messages.warning(self.request, "Please check/upload the product documentations!")
                return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))


class StockUpdateView(LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView):
    """Update view for Stock model"""

    model = Stock
    form_class = StockForm
    template_name = "stock/stock_update.html"
    success_url = reverse_lazy("stock_list")

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_class"] = "stock"
        return context


class StockListView(LoginRequiredMixin, ListView):
    """List view for Stock model"""

    model = Stock
    context_object_name = "stocks"
    template_name = "stock/stock_list.html"
    paginate_by = 8
    ordering = ["-created"]

    def get_queryset(self):
        """Filter stocks based on the 'filter' query parameter."""
        queryset = super().get_queryset()
        filter_type = self.request.GET.get("filter", "active")  # Default to non-expired

        if filter_type == "all":
            return queryset.order_by(*self.ordering)
        elif filter_type == "expired":
            return queryset.filter(expiry_date__lt=timezone.now().date()).order_by(*self.ordering)
        else:  # Default to non-expired
            return queryset.filter(expiry_date__gte=timezone.now().date()).order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_type"] = self.request.GET.get("filter", "active")
        return context


class StockDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for Stock model"""

    model = Stock
    action_url = "stock_delete"
    success_url = reverse_lazy("stock_list")


class StockDetailView(LoginRequiredMixin, DetailView):
    """Detail view for Stock model"""

    model = Stock
    context_object_name = "stock"
    template_name = "stock/stock_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attachments"] = StockAttachment.objects.filter(object_id=self.object.id)
        return context


# StockEntry CRUD Views
class StockEntryUpdateView(LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView):
    """Update view for the StockEntry model"""

    model = StockEntry
    form_class = StockEntryUpdateForm
    template_name = "stock/stock_entry_update.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_entry = self.object  # The stock entry being updated

        if stock_entry.location:
            context["location_name"] = stock_entry.location.name
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class StockEntryDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for StockEntry model"""

    model = StockEntry
    action_url = "stock_entry_delete"
    success_url = reverse_lazy("stock_list")


# Stock attachment CRUD views
class StockAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for StockAttachment model"""

    owner_model = Stock
    form_class = StockAttachmentCreateForm
    success_url_name = "stock_detail"
    template_name = "attachment/attachment_upload_form.html"


class StockAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for StockAttachment model"""

    owner_model = Stock
    model = StockAttachment
    template_name = "attachment/attachment_delete_form.html"
    success_url_name = "stock_detail"


class StockAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for StockAttachment model"""

    owner_model = Stock
    model = StockAttachment
    form_class = StockAttachmentUpdateForm
    template_name = "attachment/attachment_update_form.html"
    success_url_name = "stock_detail"


# Stock label printing views
class StockLabelPrintView(LoginRequiredMixin, LabelPrintBaseView):
    """Print view for Stock model"""

    template_name = "stock/partials/label_print_settings.html"

    def get_message_context(self) -> dict:
        """Return the context for the message"""
        base_url = self.request.build_absolute_uri("/").rstrip("/")
        stock = Stock.objects.get(pk=self.kwargs["pk"])
        entries = stock.entries.all()
        messages = {}
        for entry in entries:
            top_text = f"{stock.source.product_id} ({entry.ordinal_number})"
            bottom_text = f"{stock.lot_number}: {entry.pk}"
            message = base_url + reverse("usage_qr_update", kwargs={"pk": entry.pk})
            messages[message] = (top_text, bottom_text)
        return messages

    def get_action_url(self, *args, **kwargs) -> str:
        """Return the action url"""
        return reverse("stock_label_print", kwargs={"pk": self.kwargs["pk"]})
