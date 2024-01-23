""""Views for searching for models in the item app"""
from django.contrib.auth.mixins import LoginRequiredMixin

from core.views.generic import GenericSingleModelSearchView
from item.models import InhouseReagent, Item, Stock


class InhouseReagentSearchView(LoginRequiredMixin, GenericSingleModelSearchView):
    """View for searching for inhouse reagents"""

    model = InhouseReagent
    query_name = "inhouse_query"
    search_fields = ["name", "description", "product_id", "lot_number"]
    template_name = "inhouse/partials/search_results.html"


class ItemSearchView(LoginRequiredMixin, GenericSingleModelSearchView):
    """View for searching for items"""

    model = Item
    query_name = "item_query"
    search_fields = ["name", "description", "manufacturer__name", "supplier__name"]
    template_name = "item/partials/search_results.html"


class StockSearchView(LoginRequiredMixin, GenericSingleModelSearchView):
    """View for searching for stocks"""

    model = Stock
    query_name = "stock_query"
    search_fields = [
        "lot_number",
        "item__name",
        "item__product_id",
        "inhouse_reagent__name",
        "inhouse_reagent__product_id",
    ]
    extra_filters = {"validations__validation__status": "APPROVED"}
    template_name = "stock/partials/search_results.html"
