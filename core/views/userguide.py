"""user guide page views """

from django.views.generic import TemplateView


class UserGuideView(TemplateView):
    """User guide page view."""

    template_name = "userguide.html"
