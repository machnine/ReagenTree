""""Views for searching for models in the item app"""
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from item.models import InhouseReagent, Item, Stock


# inhouse reagent search view
@login_required
def inhouse_reagent_search(request):
    """HTMX view for returning a list of inhouse reagents"""
    query = request.GET.get("inhouse_query", "")
    if query:
        queries = [Q(name__icontains=term) | Q(description__icontains=term) for term in query.split()]
        combined_query = reduce(lambda x, y: x & y, queries)
        inhouse_reagents = InhouseReagent.objects.filter(combined_query)[:5]
    else:
        inhouse_reagents = []
    return render(request, "inhouse/partials/search_results.html", {"found_inhouse_reagents": inhouse_reagents})


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
        combined_query = reduce(lambda x, y: x & y, queries)
        items = Item.objects.filter(combined_query)[:5]
    else:
        items = []
    return render(request, "item/partials/search_results.html", {"found_items": items})


# Stock search view
@login_required
def stock_search(request):
    """HTMX GET request for returning a list of search stocks"""
    query = request.GET.get("stock_query", "")
    if query:
        queries = [
            Q(lot_number__icontains=term)
            | Q(item__name__icontains=term)
            | Q(item__product_id__icontains=term)
            | Q(inhouse_reagent__name__icontains=term)
            | Q(inhouse_reagent__product_id__icontains=term)
            for term in query.split()
        ]
        combined_query = reduce(lambda x, y: x & y, queries)
        stocks = Stock.objects.filter(combined_query, validations__validation__status="APPROVED").distinct()[:5]
    else:
        stocks = []
    return render(request, "stock/partials/search_results.html", {"found_stocks": stocks})
