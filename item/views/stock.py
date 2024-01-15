"""Stock Item views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from attachment.views import (
    AttachmentDeleteView,
    AttachmentUpdateView,
    AttachmentUploadView,
)
from core.mixins import SuccessUrlMixin, FormValidMessageMixin
from core.settings import DEBUG
from core.views.generic import ObjectDeleteHTMXView
from item.forms.stock import StockAttachmentCreateForm, StockAttachmentUpdateForm
from item.models import Stock, StockAttachment, StockEntry
from item.forms import StockForm, StockEntryFormSet, StockEntryUpdateForm
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
        context["entries"] = (
            StockEntryFormSet(self.request.POST)
            if self.request.POST
            else StockEntryFormSet()
        )
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
                        location=location,
                        stock=self.object,
                        last_updated_by=self.request.user,
                        ordinal_number=n + 1,
                    )
                    entry.save()
                return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))


class StockUpdateView(
    LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView
):
    """Update view for Stock model"""

    model = Stock
    form_class = StockForm
    template_name = "stock/stock_update.html"
    success_url = reverse_lazy("stock_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object  # The stock being updated
        if stock.item:
            context["item_name"] = stock.item.name
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class StockListView(LoginRequiredMixin, ListView):
    """List view for Stock model"""

    model = Stock
    context_object_name = "stocks"
    template_name = "stock/stock_list.html"
    paginate_by = 8
    ordering = ["-created"]


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
        context["attachments"] = StockAttachment.objects.filter(
            object_id=self.object.id
        )
        return context


# StockEntry CRUD Views
class StockEntryUpdateView(
    LoginRequiredMixin, SuccessUrlMixin, FormValidMessageMixin, UpdateView
):
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
    template_name = "stock/stock_label_print.html"
    
    def get_message_context(self) -> dict:
        """Return the context for the message"""
        if DEBUG:
            base_url = "http://172.18.1.127:8000"
        else:
            base_url = self.request.build_absolute_uri("/").rstrip("/")
        stock = Stock.objects.get(pk=self.kwargs["pk"])
        entries = stock.entries.all()
        messages = {
            f"{stock.lot_number}-{stock.pk}-{entry.ordinal_number}": base_url
            + reverse("usage_update", kwargs={"pk": entry.pk})
            for entry in entries
        }
        return messages

    def get_action_url(self, *args, **kwargs) -> str:
        """Return the action url"""
        return reverse("stock_label_print", kwargs={"pk": self.kwargs["pk"]})
