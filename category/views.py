"""Category CRUD views."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from core.mixins import SuccessUrlMixin

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


class CategoryCreateView(LoginRequiredMixin, SuccessUrlMixin, CreateView):
    """Category create view."""

    model = Category
    fields = ["name", "description"]
    template_name = "category/category_create.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        if not form.instance.description:
            form.instance.description = form.instance.name
        response = super().form_valid(form)
        messages.success(
            self.request, f"Category { form.instance.name } created successfully."
        )
        return response


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
        messages.success(request, f"Category { category.name } deleted successfully.")
        return redirect("category_list")


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


class CategoryUpdateView(LoginRequiredMixin, SuccessUrlMixin, UpdateView):
    """Category update view."""

    model = Category
    fields = ["name", "description"]
    template_name = "category/category_update.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        form.instance.last_updated = timezone.now()
        response = super().form_valid(form)
        messages.success(
            self.request, f"Category { form.instance.name } updated successfully."
        )
        return response
