"""Views for the label app."""
from io import BytesIO

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LabelPrintForm
from .printers import QRCodeLabelPDFPrinter


class LabelPrintBaseView(View):
    """
    Base view for label printing
    Override get_message_context in subclass to provide messages to the printer
    messages should be a dictionary of key value pairs
    key is the hint for the message QR code, value is the message to be encoded
    """

    form_class = LabelPrintForm
    template_name = "label/label_print_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        action_url = self.get_action_url(*args, **kwargs)
        return render(
            request, self.template_name, {"form": form, "action_url": action_url}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            printer = QRCodeLabelPDFPrinter(
                sheet=form.cleaned_data["label_sheet"],
                messages=self.get_message_context(),
                skipped=form.cleaned_data["skipped_labels"],
            )
            pdf_content = printer.print()

            if isinstance(pdf_content, BytesIO):
                pdf_content = pdf_content.getvalue()
                response = HttpResponse(pdf_content, content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="labels.pdf"'
                return response
            else:
                raise TypeError(
                    f"Unexpected type of PDF content {type(pdf_content)}: {pdf_content} when printing labels"
                )

        return render(request, self.template_name, {"form": form})

    def get_message_context(self) -> dict:
        """Default implementation, override in subclass"""
        return {"test": "This is a test message override me."}

    def get_action_url(self, *args, **kwargs) -> str:
        """Default implementation, override in subclass"""
        return "label_print"
