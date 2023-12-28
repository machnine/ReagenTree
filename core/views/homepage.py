"""Core page views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from item.models import Item, Stock


@login_required
def index(request):
    """Home page view."""
    items = Item.objects.all()
    stocks = Stock.objects.all()
    return render(request, "index.html", {"items": items, "stocks": stocks})
