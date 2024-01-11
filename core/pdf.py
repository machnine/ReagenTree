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
}


label_sheet = LabelSheet(CUSTOM_RENAL_LABEL)

messages_dict = {
    f"{i}": f"https://www.reagentree.com/usage/{i}/update/" for i in range(100, 120)
}


def pdfgen(sheet: LabelSheet, messages: dict, filename=None, skipped=0, qr_size=(15, 15), font_size=8):
    # Create a PDF buffer
    pdf_buffer = BytesIO()
    page_width, page_height = sheet.page_size

    # Create a canvas
    c = canvas.Canvas(pdf_buffer, pagesize=sheet.page_size)

    # Message iterator
    message_iter = iter(messages.items())

    # Calculate the total number of labels per page
    total_labels_per_page = sheet.label_rows * sheet.label_cols

    current_label = 0
    label_index = 0  # Index for the current label being printed

    while label_index < len(messages):
        for row in range(sheet.label_rows):
            for col in range(sheet.label_cols):
                # Only process labels if current_label >= skipped_labels
                if current_label >= skipped:
                    try:
                        hint_text, message = next(message_iter)
                        label_index += 1
                    except StopIteration:
                        break

                    # Draw the QR code
                    qr_img = generate_qr_code(message)
                    qr_buffer = BytesIO()
                    qr_img.save(qr_buffer, format="PNG")
                    qr_buffer.seek(0)

                    # QR code X position in the middle of the label
                    img_x_offset = (sheet.label_width - qr_size(0)) / 2
                    img_x_pos = (
                        sheet.margin_left
                        + (sheet.label_width + sheet.space_x) * col
                        + img_x_offset
                    )
                    # QR code Y position in the up 1/3 of the label
                    img_y_offset = (sheet.label_height - qr_size(1)) / 3 * 2
                    img_y_pos = (
                        page_height
                        - sheet.margin_top
                        - (sheet.label_height + sheet.space_y) * row
                        - qr_size(1)
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

                current_label += 1

                # Check if it's time to move to a new page
                if current_label % total_labels_per_page == 0:
                    break

            if current_label % total_labels_per_page == 0 or label_index >= len(
                messages
            ):
                # Break the outer loop as well if moving to a new page or if all messages are printed
                break

        # Start a new page if not all messages have been printed
        if label_index < len(messages):
            c.showPage()

    c.save()

    # Save or return the PDF
    if filename:
        with open(filename, "wb") as f:
            f.write(pdf_buffer.getvalue())
        return filename
    else:
        return pdf_buffer.getvalue()
