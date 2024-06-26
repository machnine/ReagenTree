"""Category CRUD views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import FormValidMessageMixin, SuccessUrlMixin
from core.views.generic import GenericSingleModelSearchView, ObjectDeleteHTMXView

from .forms import CategoryForm
from .models import Category


class CategorySearchView(LoginRequiredMixin, GenericSingleModelSearchView):
    """View for searching for a Category."""

    model = Category
    query_name = "category_query"
    search_fields = ["name", "description"]
    template_name = "category/category_search_results.html"


class CategoryCreateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, CreateView):
    """Category create view."""

    model = Category
    form_class = CategoryForm
    template_name = "category/category_form.html"
    success_url = reverse_lazy("category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_class"] = "category"
        return context


class CategoryUpdateView(LoginRequiredMixin, FormValidMessageMixin, SuccessUrlMixin, UpdateView):
    """Category update view."""

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("category_list")
    template_name = "category/category_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_class"] = "category"
        return context


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
        inhouse = self.object.inhouse_reagents.all()
        # combine items and inhouse reagents
        combined = list(items) + list(inhouse)
        # paginate items
        paginator = Paginator(combined, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    """Category list view."""

    model = Category
    context_object_name = "categories"
    template_name = "category/category_list.html"
    paginate_by = 15

    def get_queryset(self):
        query_set = super().get_queryset()
        sort_by = self.request.GET.get("sort_by", "name")
        order = self.request.GET.get("order", "asc")
        if order == "desc":
            sort_by = f"-{sort_by}"
        return query_set.order_by(sort_by)
