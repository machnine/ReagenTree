"""Core page views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from item.models import Item, Stock, WatchList


@login_required
def index(request):
    """Home page view."""
    items = Item.objects.all()
    stocks = Stock.objects.all()
    watchlists = WatchList.objects.filter(notification=True, acknowledged=None)
    context = {"items": items, "stocks": stocks, "watchlists": watchlists}
    return render(request, "index.html", context)
