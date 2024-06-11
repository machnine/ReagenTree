"""Item views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from attachment.views import AttachmentDeleteView, AttachmentUpdateView, AttachmentUploadView
from category.models import Category
from company.models import Company
from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView
from item.forms import ItemAttachmentCreateForm, ItemAttachmentUpdateForm, ItemForm
from item.models import Item, ItemAttachment, Stock


# Item CRUD views
class ItemCreateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView):
    """Create view for Item model"""

    model = Item
    form_class = ItemForm
    template_name = "item/item_form.html"
    success_url = reverse_lazy("item_list")

    def get_field_obj_name(self, field_value, obj_model):
        """Return the name of the field object."""
        if field_value:
            obj = field_value if hasattr(field_value, "id") else obj_model.objects.get(pk=field_value)
            return obj.name

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # retain the selected category, manufacturer, and supplier
        # in the form if the form is invalid for better UX

        context["category_name"] = self.get_field_obj_name(form.cleaned_data.get("category"), Category)
        context["manufacturer_name"] = self.get_field_obj_name(form.cleaned_data.get("manufacturer"), Company)
        context["supplier_name"] = self.get_field_obj_name(form.cleaned_data.get("supplier"), Company)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_class"] = "item"
        return context

class ItemUpdateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView):
    """Update view for Item model"""

    model = Item
    form_class = ItemForm
    template_name = "item/item_form.html"
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

        context["object_class"] = "item"

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


class ItemAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteView):
    """Delete view for ItemAttachment model"""

    owner_model = Item
    model = ItemAttachment
    template_name = "attachment/attachment_delete_form.html"
    success_url_name = "item_detail"


class ItemAttachmentUpdateView(LoginRequiredMixin, AttachmentUpdateView):
    """Update view for ItemAttachment model"""

    owner_model = Item
    model = ItemAttachment
    form_class = ItemAttachmentUpdateForm
    template_name = "attachment/attachment_update_form.html"
    success_url_name = "item_detail"
