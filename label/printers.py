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
    """stores the size of an image"""

    width: float
    height: float


class QRCodeLabelPDFPrinter:
    """Generate a PDF file with labels for printing"""

    def __init__(self, sheet: LabelSheet, messages: dict, filename: str = None, **kwargs):
        self.sheet = sheet
        self.page_size = getattr(pagesizes, self.sheet.page_size)
        self.messages = messages
        self.filename = filename
        self.skipped = kwargs.get("skipped", 0)
        self.qr_size = kwargs.get("qr_size", LabelImageSize(15, 15))
        self.font_size = kwargs.get("font_size", 6)
        self.qr_generator = QRCodeGenerator()

    def _get_x_offset(self, item_width: float) -> float:
        """calculate the x offset for a the QR code image (middle of the label)"""
        return (self.sheet.label_width - item_width) / 2  # in mm

    def _get_y_offset(self) -> float:
        """calculate the y offset for a the QR code image (upper 1/3 of the label)"""
        return (self.sheet.label_height - self.qr_size.height) / 3 * 2  # in mm

    def _get_x_position(self, col: int, item_width: float) -> float:
        """calculate the x position for a label"""
        return (
            self.sheet.margin_left
            + (self.sheet.label_width + self.sheet.space_x) * col
            + self._get_x_offset(item_width)
        ) * mm  # (* mm converts to pionts)

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
        qr_buffer = BytesIO()  # convert the image to a buffer
        qr_code_image.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        img_reader = ImageReader(qr_buffer)

        c.drawImage(img_reader, img_x_pos, img_y_pos, width=img_width, height=img_height)

    def _draw_hint_text(
        self,
        c: canvas.Canvas,
        col: int,
        row: int,
        text_top: str = None,
        text_bottom: str = None,
        text_font: str = "Helvetica",
    ):
        """draw texts on a label"""

        def calculate_text_position(text, row, col, offset):
            """calculate the position of a text on a label"""
            if not text:  # default position
                return self._get_x_position(col, 0), self._get_y_position(row) + offset
            text_width = c.stringWidth(text, text_font, self.font_size) / mm  # text_widtch converted to mm
            x_pos = self._get_x_position(col, text_width)
            y_pos = self._get_y_position(row) + offset
            return x_pos, y_pos

        # top text
        tt_offset = self.qr_size.height * mm - self.font_size * 0.4
        tt_x_pos, tt_y_pos = calculate_text_position(text_top, row, col, tt_offset)
        # bottom text
        bt_offset = -self.font_size / 2
        bt_x_pos, bt_y_pos = calculate_text_position(text_bottom, row, col, bt_offset)
        # set font
        c.setFont(text_font, self.font_size)
        # draw the text
        c.drawString(tt_x_pos, tt_y_pos, text_top)
        c.drawString(bt_x_pos, bt_y_pos, text_bottom)

    def _draw_grid(self, c: canvas.Canvas):
        """Draw a grid overlay for each label position with correct conversion from mm to points."""
        c.setStrokeColorRGB(0.5, 0.5, 0.5)  # Set a visible color for the grid

        # Loop through rows and columns to draw the grid, ensuring all measurements are in points
        for row in range(self.sheet.label_rows):
            for col in range(self.sheet.label_cols):
                x_pos = self.sheet.margin_left * mm + (self.sheet.label_width + self.sheet.space_x) * col * mm
                y_pos = (
                    self.page_size[1]
                    - self.sheet.margin_top * mm
                    - (self.sheet.label_height + self.sheet.space_y) * row * mm
                )
                width = self.sheet.label_width * mm
                height = self.sheet.label_height * mm

                # Ensure y position is calculated from the bottom of the label, converting y_pos to the bottom left corner
                c.rect(x_pos, y_pos - height, width, height)

    def print(self, drw_grid: bool = False):
        """create and position label on PDF"""

        pdf_buffer = BytesIO()  # buffer for the PDF
        c = canvas.Canvas(pdf_buffer, pagesize=self.page_size)  # canvas
        message_iter = iter(self.messages.items())  # message iterator
        current_label = 0  # current label number
        label_index = 0  # index for the current label being printed

        while label_index < len(self.messages):
            if drw_grid:
                self._draw_grid(c)

            for row in range(self.sheet.label_rows):
                for col in range(self.sheet.label_cols):
                    # only process if the current label >= skipped labels
                    if current_label >= self.skipped:
                        try:
                            message, hint = next(message_iter)
                            top_hint, bottom_hint = hint
                            label_index += 1
                        except StopIteration:
                            break

                        self._draw_qr_code(c, message, col, row)  # draw the QR code
                        self._draw_hint_text(c, col, row, top_hint, bottom_hint)  # draw the hint text

                    current_label += 1  # increment the current label number
                    # check if we reached the end of the page
                    if current_label % self.sheet.labels_per_sheet == 0:
                        break
                # Break the outer loop as well if moving to a new page or if all messages are printed
                if current_label % self.sheet.labels_per_sheet == 0 or label_index >= len(self.messages):
                    break
            # Start a new page if not all messages are printed
            if label_index < len(self.messages):
                c.showPage()

        c.save()  # save the PDF
        pdf_buffer.seek(0)  # reset the buffer

        # Save or return the PDF
        if self.filename:
            with open(self.filename, "wb") as f:
                f.write(pdf_buffer.getvalue())
            return self.filename
        else:
            return pdf_buffer
