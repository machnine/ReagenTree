""" Sitewide search views """
from django.db.models import Q
from django.views.generic import ListView


class GenericSingleModelSearchView(ListView):
    """Generic view for searching a single model"""

    model = None
    query_name = None
    search_fields = []
    extra_filters = {}
    template_name = None
    context_object_limit = 5
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
        return self.model.objects.filter(base_query, **self.extra_filters).distinct()[: self.context_object_limit]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get(self.query_name, "")
        return context
