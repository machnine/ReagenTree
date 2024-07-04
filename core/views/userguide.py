"""user guide page views """

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class UserGuideView(LoginRequiredMixin, TemplateView):
    """User guide page view."""

    template_name = "userguide_page.html"
