"""Item views"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from attachment.views import (
    AttachmentUploadView,
    AttachmentDeleteView,
    AttachmentUpdateView,
)
from core.mixins import SuccessUrlMixin, FormValidMessageMixin
from core.views.generic import ObjectDeleteHTMXView
from category.models import Category
from company.models import Company
from item.models import Item, ItemAttachment, Stock
from item.forms import ItemForm, ItemAttachmentCreateForm, ItemAttachmentUpdateForm


# Item search view
@login_required
def item_search(request):
    """HTMX GET request for returning a list of search items"""
    query = request.GET.get("item_query", "")
    if query:
        queries = [
            Q(name__icontains=term)
            | Q(description__icontains=term)
            | Q(manufacturer__name__icontains=term)
            | Q(supplier__name__icontains=term)
            for term in query.split()
        ]
        query = queries.pop()
        for item in queries:
            query &= item
        items = Item.objects.filter(query)[:5]
    else:
        items = []
    return render(request, "item/item_search_results.html", {"found_items": items})


# Item CRUD views
class ItemCreateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView
):
    """Create view for Item model"""

    model = Item
    form_class = ItemForm
    template_name = "item/item_create.html"
    success_url = reverse_lazy("item_list")

    def get_field_obj_name(self, field_value, obj_model):
        """Return the name of the field object."""
        if field_value:
            obj = (
                field_value
                if hasattr(field_value, "id")
                else obj_model.objects.get(pk=field_value)
            )
            return obj.name

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # retain the selected category, manufacturer, and supplier
        # in the form if the form is invalid for better UX

        context["category_name"] = self.get_field_obj_name(
            form.cleaned_data.get("category"), Category
        )
        context["manufacturer_name"] = self.get_field_obj_name(
            form.cleaned_data.get("manufacturer"), Company
        )
        context["supplier_name"] = self.get_field_obj_name(
            form.cleaned_data.get("supplier"), Company
        )
        return self.render_to_response(context)


class ItemUpdateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView
):
    """Update view for Item model"""

    model = Item
    form_class = ItemForm
    template_name = "item/item_update.html"
    success_url = reverse_lazy("item_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object  # The item being updated

        if item.category:
            context["category_name"] = item.category.name
        if item.manufacturer:
            context["manufacturer_name"] = item.manufacturer.name
        if item.supplier:
            context["supplier_name"] = item.supplier.name

        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class ItemDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Delete view for Item model"""

    model = Item
    action_url = "item_delete"
    success_url = reverse_lazy("item_list")


class ItemDetailView(LoginRequiredMixin, DetailView):
    """Detail view for Item model"""

    model = Item
    context_object_name = "item"
    template_name = "item/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stocks"] = Stock.objects.filter(item=self.object)
        context["attachments"] = ItemAttachment.objects.filter(object_id=self.object.id)
        return context


class ItemListView(LoginRequiredMixin, ListView):
    """List view for Item model"""

    model = Item
    context_object_name = "items"
    template_name = "item/item_list.html"
    paginate_by = 15


#
# Item attachment CRUD views
#
class ItemAttachmentUploadView(LoginRequiredMixin, AttachmentUploadView):
    """Upload view for ItemAttachment model"""

    owner_model = Item
    form_class = ItemAttachmentCreateForm
    success_url_name = "item_detail"
    template_name = "attachment/attachment_upload_form.html"
    upload_url_name = "item_attachment_upload"


class ItemAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for ItemAttachment model"""

    model = ItemAttachment
    template_name = "item/item_detail_attachment_delete.html"
    success_url_name = "item_detail"


class ItemAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for ItemAttachment model"""

    model = ItemAttachment
    form_class = ItemAttachmentUpdateForm
    template_name = "item/item_detail_attachment_update.html"
    success_url_name = "item_detail"
