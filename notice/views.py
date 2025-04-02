"""Views for the Notice app."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .forms import NoticeForm
from .models import Notice


class NoticeListView(LoginRequiredMixin, ListView):
    """List all notices (active and archived)."""

    model = Notice
    template_name = "notice/notice_list.html"
    context_object_name = "notices"
    paginate_by = 15

    def get_queryset(self):
        """Filter notices based on archive status and handle sorting."""
        query_set = Notice.objects.all()  # Start with all notices

        # Filter by archive status
        archive_status = self.request.GET.get("archive", "active")  # Default to active
        if archive_status == "archived":
            query_set = query_set.filter(is_archived=True)
        else:
            query_set = query_set.filter(is_archived=False)

        # Handle sorting
        sort_by = self.request.GET.get("sort_by", "created_at")
        order = self.request.GET.get("order", "desc")

        if sort_by == "created_by":
            sort_by = "created_by__username"  # Sort by username
        elif sort_by == "importance":
            sort_by = "importance"  # Sort by importance
        elif sort_by == "message":
            sort_by = "message"
        elif sort_by == "expiry_date":
            sort_by = "expiry_date"
        elif sort_by == "created_at":
            sort_by = "created_at"
        else:
            sort_by = "created_at"

        if order == "desc":
            sort_by = f"-{sort_by}"

        return query_set.order_by(sort_by)

    def get_context_data(self, **kwargs):
        """Add archive status to the context."""
        context = super().get_context_data(**kwargs)
        archive_status = self.request.GET.get("archive", "active")
        context["archive_status"] = archive_status
        return context


class NoticeDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a single notice."""

    model = Notice
    template_name = "notice/notice_detail.html"
    context_object_name = "notice"


class NoticeCreateView(LoginRequiredMixin, CreateView):
    """Create a new notice."""

    model = Notice
    form_class = NoticeForm
    template_name = "notice/notice_form.html"
    success_url = reverse_lazy("notice_list")

    def form_valid(self, form):
        """Set the created_by user."""
        form.instance.created_by = self.request.user
        messages.success(self.request, "Notice created successfully.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_class"] = "notice"
        return context



class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing notice."""

    model = Notice
    form_class = NoticeForm
    template_name = "notice/notice_form.html"
    success_url = reverse_lazy("notice_list")

    def form_valid(self, form):
        """Set the updated_by user."""
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Notice updated successfully.")
        return super().form_valid(form)


class NoticeArchiveView(LoginRequiredMixin, View):
    """Archive/Unarchive a notice."""

    def post(self, request, *args, **kwargs):
        """Toggle the archive status of the notice."""
        with transaction.atomic():
            notice = get_object_or_404(Notice, pk=kwargs["pk"])
            notice.is_archived = not notice.is_archived  # Toggle the status
            notice.save()
            if notice.is_archived:
                messages.success(request, "Notice archived successfully.")
            else:
                messages.success(request, "Notice unarchived successfully.")

        # Redirect to the correct list view (active or archived)
        archive_status = request.GET.get("archive", "active")
        redirect_url = reverse_lazy("notice_list") + f"?archive={archive_status}"
        headers = {
            "HX-Redirect": redirect_url,
        }
        return HttpResponse(headers=headers)
