""" Mixins """
class SuccessUrlMixin:
    """Success Url Mixin"""

    def get_success_url(self):
        """return the URL to redirect to, after processing a valid form."""

        if next_url := self.request.POST.get("next"):
            print("called.. NEXT URL ..")
            return next_url
        else:
            print("called.. SUCC URL ..")
            return super().get_success_url()
