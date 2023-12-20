"""Stock usage views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404

from item.models import Stock, Usage
from item.forms import UsageForm


class UsageCreateView(LoginRequiredMixin, CreateView):
    """Create a new usage record."""

    model = Usage
    form_class = UsageForm
    template_name = "item/usage_create.html"
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.stock = get_object_or_404(Stock, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usage_by = self.request.user
        form.instance.stock = self.stock
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stock"] = self.stock
        return context
