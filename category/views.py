"""Category CRUD views."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from core.mixins import SuccessUrlMixin

from .models import Category


class CategoryCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Category create view."""

    model = Category
    fields = ["name", "description"]
    template_name = "category/category_create.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, View):
    """Category delete view."""

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning a Category delete form."""
        category = Category.objects.get(pk=kwargs["pk"])
        return render(
            request, "category/category_delete_form.html", {"category": category}
        )

    def post(self, request, *args, **kwargs):
        """Handle POST request."""
        category = Category.objects.get(pk=kwargs["pk"])
        category.delete()
        return redirect("category_list")


class CategoryDetailView(LoginRequiredMixin, DetailView):
    """Category detail view."""

    model = Category
    template_name = "category/category_detail.html"


class CategoryListView(LoginRequiredMixin, ListView):
    """Category list view."""

    model = Category
    context_object_name = "categories"
    template_name = "category/category_list.html"
    paginate_by = 5


class CategoryUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """Category update view."""

    model = Category
    fields = ["name", "description"]
    template_name = "category/category_update.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        return super().form_valid(form)
