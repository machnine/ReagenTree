"""Views for the attachment app."""
from pathlib import Path

from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DeleteView


class AttachmentUploadView(View):
    """Generic view to upload attachments to a given object."""

    owner_model = None
    form_class = None
    template_name = None
    success_url_name = None

    def get(self, request, pk):
        obj = get_object_or_404(self.owner_model, pk=pk)
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "object": obj})

    def post(self, request, pk):
        obj = get_object_or_404(self.owner_model, pk=pk)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.content_object = obj
            attachment.save()
            return redirect(reverse_lazy(self.success_url_name, kwargs={"pk": obj.pk}))
        return render(request, self.template_name, {"form": form, "object": obj})


class AttachmentEditView(View):
    """Generic view to edit attachments associated with a given object."""

    model = None
    form_class = None
    template_name = None
    success_url_name = None

    def get(self, request, pk):
        attachment = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=attachment)
        return render(
            request, self.template_name, {"form": form, "attachment": attachment}
        )

    def post(self, request, pk):
        attachment = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=attachment)
        if form.is_valid():
            attachment = form.save()
            return redirect(
                reverse_lazy(self.success_url_name, kwargs={"pk": attachment.object_id})
            )
        return render(
            request, self.template_name, {"form": form, "attachment": attachment}
        )


class AttachmentDeleteView(DeleteView):
    """Generic view to delete attachments associated with a given object."""

    model = None
    template_name = None
    success_url_name = None
    context_object_name = "attachment"

    def form_valid(self, form):
        """If the form is valid, delete the associated file and then the object."""
        if self.object.file:
            file_path = Path(settings.MEDIA_ROOT) / self.object.file.name
            if file_path.is_file():
                file_path.unlink()
        return super().form_valid(form)

    def get_success_url(self):
        # Get the id of the related object before the attachment is deleted
        related_object_id = self.object.content_object.id
        return reverse(self.success_url_name, kwargs={"pk": related_object_id})
