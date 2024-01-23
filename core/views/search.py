""" Site wide search views"""
from category.models import Category
from company.models import Company
from item.models import InhouseReagent, Item, ItemAttachment, Stock, StockAttachment
from location.models import Location

from .generic import GenericMultiModelSearchView

# Aggregate all searchable models
search_models = [Category, Company, Item, Location, InhouseReagent, ItemAttachment, StockAttachment, Stock]
# common search fields
search_config = {f"{model.__name__.lower()}": ["name", "description"] for model in search_models}
# Add additional search fields
search_config["location"] += ["room__name"]
search_config["inhousereagent"] += ["product_id", "lot_number", "category__name"]
search_config["item"] += ["product_id", "cas_number", "category__name", "manufacturer__name", "supplier__name"]
# assign search fields to Stock, removing the default name and description as well
search_config["stock"] = [
    "lot_number",
    "item__name",
    "item__product_id",
    "inhouse_reagent__name",
    "inhouse_reagent__product_id",
    "comments",
]


class SiteWideSearchView(GenericMultiModelSearchView):
    """Site-wide search view"""

    template_name = "partials/site_wide_search.html"

    # Aggregate all search configurations
    search_models = [(model, search_config[model.__name__.lower()]) for model in search_models]
