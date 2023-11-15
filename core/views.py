"""Core views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    """Home page view."""
    return render(request, "index.html")
