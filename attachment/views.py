"""Views for the attachment app."""
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View


class AttachmentUploadView(View):
    """Generic view to upload attachments to a given object."""

    owner_model = None
    form_class = None
    template_name = None
    success_url_name = None
    upload_url_name = None

    def get(self, request, pk):
        obj = get_object_or_404(self.owner_model, pk=pk)
        form = self.form_class()
        upload_url = reverse_lazy(self.upload_url_name, kwargs={"pk": obj.pk})
        return render(
            request,
            self.template_name,
            {"form": form, "object": obj, "upload_url": upload_url},
        )

    def post(self, request, pk):
        obj = get_object_or_404(self.owner_model, pk=pk)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.content_object = obj
            attachment.save()
            messages.success(
                request, f"Attachment {attachment.filename} uploaded successfully!"
            )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Upload {field.capitalize()}: {error}")
        return redirect(reverse_lazy(self.success_url_name, kwargs={"pk": obj.pk}))


class AttachmentUpdateView(View):
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
            messages.success(
                request, f"Attachment {attachment.filename} updated successfully!"
            )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Upload {field.capitalize()}: {error}")
        return redirect(
            reverse_lazy(self.success_url_name, kwargs={"pk": attachment.object_id})
        )


class AttachmentDeleteView(View):
    """HTMX powered view to delete attachments associated with a given object."""

    model = None  # a specific child model of Attachment
    template_name = None
    success_url_name = None

    def get(self, request, *args, **kwargs):
        """HTMX GET request for returning an Attachment delete form."""
        attachment = get_object_or_404(self.model, pk=kwargs["pk"])
        return render(
            request,
            self.template_name,
            {"attachment": attachment},
        )

    def post(self, request, *args, **kwargs):
        """HTMX POST request for deleting an Attachment."""
        attachment = get_object_or_404(self.model, pk=kwargs["pk"])
        # delete from the database
        owner_object_id = (
            attachment.object_id
        )  # get the id of the related object before the attachment is deleted
        attachment.delete()
        # Delete the file from the file system
        file_path = Path(settings.MEDIA_ROOT) / attachment.file.name
        if file_path.is_file():
            file_path.unlink()
        messages.success(
            request, f"Attachment {attachment.filename} deleted successfully!"
        )

        return redirect(self.get_owner_redirect_url(owner_object_id))

    def get_owner_redirect_url(self, owner_object_id):
        """Return the url to redirect to after the attachment is deleted."""
        return reverse_lazy(self.success_url_name, kwargs={"pk": owner_object_id})
