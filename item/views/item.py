"""Item views"""

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

from item.models import Item


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
class ItemCreateView(LoginRequiredMixin, CreateView):
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

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""

        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        return super().form_valid(form)


class ItemDetailView(LoginRequiredMixin, DetailView):
    """Detail view for Item model"""

    model = Item
    context_object_name = "item"
    template_name = "item/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stockitems"] = self.object.stockitems.all()
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
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
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        return super().form_valid(form)


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
        return redirect("item_list")


class ItemListView(LoginRequiredMixin, ListView):
    """List view for Item model"""

    model = Item
    context_object_name = "items"
    template_name = "item/item_list.html"
