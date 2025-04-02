"""Core page views."""

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from item.models import Stock, WatchList
from notice.models import Notice


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
    # Get active notices
    notices = Notice.objects.filter(is_archived=False, expiry_date__gte=timezone.now()).order_by(
        "-importance", "-created_at"
    )
    context = {"stocks": stocks, "watchlists": watchlists, "validations": validations, "notices": notices}
    return render(request, "index.html", context)
