from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.lib.utils import ImageReader
from .labels import generate_qr_code


class LabelSheet:
    def __init__(self, config):
        self.page_size = config.get("page_size")
        self.label_width = config.get("label_width")
        self.label_height = config.get("label_height")
        self.label_rows = config.get("label_rows")
        self.label_cols = config.get("label_cols")
        self.margin_left = config.get("margin_left")
        self.margin_right = config.get("margin_right")
        self.margin_top = config.get("margin_top")
        self.margin_bottom = config.get("margin_bottom")
        self.space_x = config.get("space_x")
        self.space_y = config.get("space_y")
        self.qr_width = config.get("qr_width")
        self.qr_height = config.get("qr_height")
        self.font_size = config.get("font_size")
        self.skipped_labels = config.get("skipped_labels")


CUSTOM_RENAL_LABEL = {
    "page_size": A4,
    "margin_left": 8 * mm,
    "margin_right": 7 * mm,
    "margin_top": 4 * mm,
    "margin_bottom": 7 * mm,
    "label_rows": 10,
    "label_cols": 6,
    "label_width": 30 * mm,
    "label_height": 26 * mm,
    "space_x": 3 * mm,
    "space_y": 3 * mm,
    "qr_width": 15 * mm,
    "qr_height": 15 * mm,
    "font_size": 8
}


label_sheet = LabelSheet(CUSTOM_RENAL_LABEL)

messages_dict = {
    f"{i}": f"https://www.reagentree.com/usage/{i}/update/" for i in range(100, 120)
}


def pdfgen(sheet: LabelSheet, messages: dict, filename=None, skipped_labels=0):
    # Create a PDF buffer
    pdf_buffer = BytesIO()
    page_width, page_height = sheet.page_size

    # Create a canvas
    c = canvas.Canvas(pdf_buffer, pagesize=sheet.page_size)

    # message iterator
    message_iter = iter(messages.items())

    row_start = skipped_labels // sheet.label_cols
    row_end = sheet.label_rows
    col_start = skipped_labels % sheet.label_cols
    col_end = sheet.label_cols

    for row in range(row_start, row_end):
        for col in range(col_start, col_end):
            # message
            try:
                hint_text, message = next(message_iter)
            except StopIteration:
                break
            # Draw the QR code
            qr_img = generate_qr_code(message)
            qr_buffer = BytesIO()
            qr_img.save(qr_buffer, format="PNG")
            qr_buffer.seek(0)

            # QR code X position in the middle of the label
            img_x_offset = (sheet.label_width - sheet.qr_width) / 2
            img_x_pos = (
                sheet.margin_left
                + (sheet.label_width + sheet.space_x) * col
                + img_x_offset
            )
            # QR code Y position in the up 1/3 of the label
            img_y_offset = (sheet.label_height - sheet.qr_height) / 3 * 2
            img_y_pos = (
                page_height
                - sheet.margin_top
                - (sheet.label_height + sheet.space_y) * row
                - sheet.qr_height
                - img_y_offset
            )

            c.drawImage(
                ImageReader(qr_buffer),
                img_x_pos,
                img_y_pos,
                width=sheet.qr_width,
                height=sheet.qr_height,
            )

            # Draw the hint text
            text_width = c.stringWidth(hint_text, "Helvetica", sheet.font_size)
            txt_x_offset = (sheet.label_width - text_width) / 2
            txt_x_pos = (
                sheet.margin_left
                + (sheet.label_width + sheet.space_x) * col
                + txt_x_offset
            )
            txt_y_pos = img_y_pos - sheet.font_size
            c.setFont("Helvetica", sheet.font_size)
            c.drawString(txt_x_pos, txt_y_pos, hint_text)

    c.save()
    # Save or return the PDF
    if filename:
        with open(filename, "wb") as f:
            f.write(pdf_buffer.getvalue())
        return filename
    else:
        return pdf_buffer.getvalue()
