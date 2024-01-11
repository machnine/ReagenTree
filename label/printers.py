""" Label sheet generator (in PDF format) """
from dataclasses import dataclass
from io import BytesIO

from reportlab.lib import pagesizes
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


from label.models import LabelSheet
from label.qr_code import QRCodeGenerator


@dataclass
class LabelImageSize:
    """stores the size of an image and provide px to mm conversion"""

    width: float
    height: float


class QRCodeLabelPDFPrinter:
    """Generate a PDF file with labels for printing"""

    def __init__(
        self, sheet: LabelSheet, messages: dict, filename: str = None, **kwargs
    ):
        self.sheet = sheet
        self.page_size = getattr(pagesizes, self.sheet.page_size)
        self.messages = messages
        self.filename = filename
        self.skipped = kwargs.get("skipped", 0)
        self.qr_size = kwargs.get("qr_size", LabelImageSize(15, 15))
        self.font_size = kwargs.get("font_size", 8)
        self.qr_generator = QRCodeGenerator()

    def _get_x_offset(self, width: float) -> float:
        """calculate the x offset for a the QR code image (middle of the label)"""        
        return (self.sheet.label_width - width) / 2 # in mm

    def _get_y_offset(self) -> float:
        """calculate the y offset for a the QR code image (upper 1/3 of the label)"""
        return (self.sheet.label_height - self.qr_size.height) / 3 * 2 # in mm

    def _get_x_position(self, col: int, width: float) -> float:
        """calculate the x position for a label"""
        return (
            self.sheet.margin_left
            + (self.sheet.label_width + self.sheet.space_x) * col
            + self._get_x_offset(width)
        ) * mm # (* mm converts to pionts)

    def _get_y_position(self, row: int):
        """calculate the y position for a label"""
        # converting str size name (e.g "A4") to reportlab size (mm tuple)
        _page_width, page_height = self.page_size
        return (
            page_height
            - (
                self.sheet.margin_top
                + (self.sheet.label_height + self.sheet.space_y) * row
                + self.qr_size.height
                + self._get_y_offset()
            )
            * mm
        )  # (* mm converts to pionts)

    def _draw_qr_code(self, c: canvas.Canvas, message: str, col: int, row: int):
        """draw a QR code on a label"""
        # position and generate the QR code
        img_x_pos = self._get_x_position(col, self.qr_size.width)
        img_y_pos = self._get_y_position(row)
        img_width = self.qr_size.width * mm
        img_height = self.qr_size.height * mm

        # draw the QR code on the PDF
        qr_code_image = self.qr_generator.make(message).image
        # convert the image to a buffer
        qr_buffer = BytesIO()
        qr_code_image.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        img_reader = ImageReader(qr_buffer)

        c.drawImage(
            img_reader,
            img_x_pos,
            img_y_pos,
            width=img_width,
            height=img_height,
        )

    def _draw_hint_text(self, c: canvas.Canvas, hint_text: str, col: int, row: int):
        """draw a hint text on a label"""
        # text_widtch converted to mm
        text_width = c.stringWidth(hint_text, "Helvetica", self.font_size) / mm 
        txt_x_pos = self._get_x_position(col, text_width)
        txt_y_pos = self._get_y_position(row) - self.font_size

        # draw the hint text on the PDF
        c.setFont("Helvetica", self.font_size)
        c.drawString(txt_x_pos, txt_y_pos, hint_text)

    def print(self):
        """create and position label on PDF"""

        # buffer
        pdf_buffer = BytesIO()
        # canvas
        c = canvas.Canvas(pdf_buffer, pagesize=self.page_size)
        # message iterator
        message_iter = iter(self.messages.items())
        # current label number
        current_label = 0
        # index for the current label being printed
        label_index = 0

        while label_index < len(self.messages):
            for row in range(self.sheet.label_rows):
                for col in range(self.sheet.label_cols):
                    # only process if the current label >= skipped labels
                    if current_label >= self.skipped:
                        try:
                            hint, message = next(message_iter)
                            label_index += 1
                        except StopIteration:
                            break

                        # draw the QR code
                        self._draw_qr_code(c, message, col, row)
                        # draw the hint text
                        self._draw_hint_text(c, hint, col, row)

                    # increment the current label number
                    current_label += 1
                    # check if we reached the end of the page
                    if current_label % self.sheet.labels_per_sheet == 0:
                        break
                # Break the outer loop as well if moving to a new page or if all messages are printed
                if (
                    current_label % self.sheet.labels_per_sheet == 0
                    or label_index >= len(self.messages)
                ):
                    break
            # Start a new page if not all messages are printed
            if label_index < len(self.messages):
                c.showPage()

        # save the PDF
        c.save()

        # reset the buffer
        pdf_buffer.seek(0)

        # Save or return the PDF
        if self.filename:
            with open(self.filename, "wb") as f:
                f.write(pdf_buffer.getvalue())
            return self.filename
        else:
            return pdf_buffer
