"""Core page views."""

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from item.models import Stock, WatchList


@login_required
def index(request):
    """Home page view."""
    stocks = Stock.objects.order_by("-delivery_date")
    # update time based watchlists
    for w in WatchList.objects.filter(notification=False, threshold_type="T"):
        w.check_and_update()
    watchlists = WatchList.objects.filter(notification=True, acknowledged=None)
    validations = Stock.objects.filter(
        Q(validations__validation__status="PENDING") | Q(validations__isnull=True)
    ).order_by("delivery_date")
    context = {"stocks": stocks, "watchlists": watchlists, "validations": validations}
    return render(request, "index.html", context)
