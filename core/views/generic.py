""" generic views for the project """
from functools import reduce

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View

from core.mixins import SuccessUrlMixin


class GenericSingleModelSearchView(ListView):
    """Generic view for searching a single model"""

    limit = 5
    model = None
    query_name = None
    search_fields = []
    extra_filters = {}
    template_name = None
    context_object_name = "search_results"

    def get_queryset(self):
        query = self.request.GET.get(self.query_name, "")
        if not query:
            return self.model.objects.none()
        # Split the query into individual terms
        terms = query.split()
        # Start with a base query
        base_query = Q()
        # For each term, add a combined Q object for all search fields
        for term in terms:
            term_query = Q(**{f"{self.search_fields[0]}__icontains": term})
            for field in self.search_fields[1:]:
                term_query |= Q(**{f"{field}__icontains": term})
            base_query &= term_query  # Combine with the base query using AND
        return self.model.objects.filter(base_query, **self.extra_filters).distinct()[: self.limit]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get(self.query_name, "")
        return context


class GenericMultiModelSearchView(View):
    """Generic view for searching multiple models"""

    limit = 5
    search_models = []
    template_name = None

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")
        context = {"query": query, "search_results": {}}

        if query:
            for model, search_fields in self.search_models:
                queries = []
                for term in query.split():
                    term_queries = [Q(**{f"{field}__icontains": term}) for field in search_fields]
                    combined_query = reduce(lambda x, y: x | y, term_queries)
                    queries.append(combined_query)

                base_query = reduce(lambda x, y: x & y, queries)
                results = model.objects.filter(base_query).distinct()[: self.limit]
                context["search_results"][model.__name__.lower()] = results

        return render(request, self.template_name, context)


class ObjectDeleteHTMXView(SuccessUrlMixin, View):
    """Generic HTMX view for deleting an object."""

    model = None
    action_url = None
    success_url = None
    template_name = "partials/object_delete_form.html"

    def get_success_url(self):
        """Return the URL to redirect to, after processing a valid form."""
        if next_url := self.request.POST.get("next"):
            return next_url
        else:
            return self.success_url

    def get_object(self, pk):
        """Return the object the view is displaying."""
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning an object delete form."""
        obj = self.get_object(kwargs["pk"])
        action_url = reverse_lazy(self.action_url, kwargs={"pk": obj.pk})
        return render(request, self.template_name, {"object": obj, "action_url": action_url})

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an object."""
        with transaction.atomic():
            obj = self.get_object(kwargs["pk"])
            obj.delete()
            messages.success(request, f"{obj} deleted successfully.")
        return redirect(self.get_success_url())
