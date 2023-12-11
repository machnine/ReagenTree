"""Item views"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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

from attachment.views import AttachmentUploadView, AttachmentDeleteHtmxView
from core.mixins import SuccessUrlMixin
from item.models import Item, ItemAttachment
from item.forms import ItemAttachmentForm
from item.mixins import ItemDetailContextMixin


# Item search view
@login_required
def item_search(request):
    """HTMX GET request for returning a list of search items"""
    query = request.GET.get("item_query", "")
    if query:
        queries = [
            Q(name__icontains=term) | Q(description__icontains=term)
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
class ItemCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Create view for Item model"""

    model = Item
    fields = [
        "name",
        "product_id",
        "description",
        "category",
        "manufacturer",
        "supplier",
    ]
    template_name = "item/item_create.html"
    success_url = reverse_lazy("item_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Item {form.instance.name} created successfully."
        )
        return response


class ItemDetailView(LoginRequiredMixin, ItemDetailContextMixin, DetailView):
    """Detail view for Item model"""

    model = Item
    context_object_name = "item"
    template_name = "item/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the context from the mixin
        context.update(self.get_item_detail_context(self.object))
        return context


class ItemUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """Update view for Item model"""

    model = Item
    fields = [
        "name",
        "product_id",
        "description",
        "category",
        "manufacturer",
        "supplier",
    ]
    template_name = "item/item_update.html"
    success_url = reverse_lazy("item_list")

    def form_valid(self, form):
        # set the last_updated_by and last_updated fields
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Item {form.instance.name} updated successfully."
        )
        return response


class ItemDeleteView(LoginRequiredMixin, View):
    """Delete view for Item model"""

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning an Item delete form."""
        item = Item.objects.get(pk=kwargs["pk"])
        return render(request, "item/item_delete_form.html", {"item": item})

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an Item."""
        item = Item.objects.get(pk=kwargs["pk"])
        item.delete()
        messages.success(request, f"Item {item.name} deleted successfully.")
        return redirect("item_list")


class ItemListView(LoginRequiredMixin, ListView):
    """List view for Item model"""

    model = Item
    context_object_name = "items"
    template_name = "item/item_list.html"
    paginate_by = 16


# Item attachment CRUD views
class ItemAttachmentUploadView(
    LoginRequiredMixin, ItemDetailContextMixin, AttachmentUploadView
):
    """Upload view for ItemAttachment model"""

    owner_model = Item
    form_class = ItemAttachmentForm
    success_url_name = "item_detail"
    template_name = "item/item_detail.html"

    def post(self, request, pk):
        """override the post method because this is not a independent view"""
        obj = self.get_owner_object(pk=pk)
        form = self.form_class(request.POST, request.FILES)
        # if form is valid save the attachment and redirect to success url
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.content_object = obj
            attachment.save()
            messages.success(
                request, f"Attachment {attachment.filename} upload successful!"
            )
        # if form is invalid, add the error messages to the messages framework and redirect to success url
        # the messages framework will display the errors in the template
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
            for field in form:
                for error in field.errors:
                    messages.error(request, f"Upload failed: {field.label}: {error}")
        return redirect(reverse_lazy(self.success_url_name, kwargs={"pk": pk}))


class ItemAttachmentDeleteView(LoginRequiredMixin, AttachmentDeleteHtmxView):
    """Delete view for ItemAttachment model"""

    model = ItemAttachment
    template_name = "item/item_detail_attachment_delete_form.html"
    success_url_name = "item_detail"
