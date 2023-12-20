"""Category CRUD views."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import ObjectDeleteHTMXView

from .models import Category


# Category search view
@login_required
def category_search(request):
    """HTMX GET request for returning a list of search categories"""
    query = request.GET.get("category_query", "")
    if query:
        queries = [
            Q(name__icontains=term) | Q(description__icontains=term)
            for term in query.split()
        ]
        query = queries.pop()
        for category in queries:
            query &= category
        categories = Category.objects.filter(query)[:5]
    else:
        categories = []
    return render(
        request,
        "category/category_search_results.html",
        {"found_categories": categories},
    )


class CategoryCreateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView
):
    """Category create view."""

    model = Category
    is_created = True
    fields = ["name", "description"]
    template_name = "category/category_create.html"
    success_url = reverse_lazy("category_list")
    form_valid_message = "Category successfully created."


class CategoryUpdateView(
    LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView
):
    """Category update view."""

    model = Category
    is_updated = True
    fields = ["name", "description"]
    success_url = reverse_lazy("category_list")
    template_name = "category/category_update.html"
    form_valid_message = "Category successfully updated."


class CategoryDeleteView(LoginRequiredMixin, ObjectDeleteHTMXView):
    """Category delete view."""

    model = Category
    action_url = "category_delete"
    success_url = reverse_lazy("category_list")


class CategoryDetailView(LoginRequiredMixin, DetailView):
    """Category detail view."""

    model = Category
    template_name = "category/category_detail.html"
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get items for pagination
        items = self.object.items.all()
        # paginate items
        paginator = Paginator(items, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    """Category list view."""

    model = Category
    context_object_name = "categories"
    template_name = "category/category_list.html"
    paginate_by = 5
