"""Help views."""

from urllib.parse import urlparse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HelpView(LoginRequiredMixin, TemplateView):
    """Help view."""

    template_name = "help/helppage.html"

    # get the referring url and workout which page calls this view then render the correct help page
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referrer_url = self.request.META.get("HTTP_REFERER", "")
        context["help_content"] = self.get_help_content(referrer_url)
        return context

    def get_help_content(self, referrer_url):
        """Get the help page for the referrer."""
        content_name = self.get_help_content_name(referrer_url)
        return f"help/{content_name}.html"

    def get_help_content_name(self, referrer_url):
        """Get the template key for the referrer."""
        url = urlparse(referrer_url)
        # Return "homepage" if the referrer path is the root
        if url.path == "/":
            return "homepage"

        # Split the referrer path into parts, excluding empty strings
        parts = [x for x in url.path.split("/") if x]

        # Filter out numeric parts from the path
        cleaned_parts = [x for x in parts if not x.isnumeric()]

        # If numeric parts are filtered out and "update" is not in the original parts
        if len(parts) != len(cleaned_parts) and "update" not in parts:
            return "_".join(cleaned_parts + ["detail"])
        else:
            return "_".join(cleaned_parts)
