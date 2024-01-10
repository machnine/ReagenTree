"""QR code label generator"""
from io import BytesIO
from qrcode import constants, QRCode
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def generate_qr_code(message, filename=None, error_correction="M"):
    """
    Generate QR Code
    'L' - About 7% or fewer errors can be corrected.
    'M' (default) - About 15% or fewer errors can be corrected.
    'Q' - About 25% or fewer errors can be corrected.
    'H' - About 30% or fewer errors can be corrected.
    """
    CORRECTIONS = {
        "L": constants.ERROR_CORRECT_L,
        "M": constants.ERROR_CORRECT_M,
        "Q": constants.ERROR_CORRECT_Q,
        "H": constants.ERROR_CORRECT_H,
    }
    qr = QRCode(
        version=1,
        error_correction=CORRECTIONS.get(error_correction, constants.ERROR_CORRECT_M),
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    if filename:
        img.save(filename)
    return img


def generate_pdf_for_qr_codes(
    messages,  # Dict of messages where each message is a string to be encoded into a QR code.
    filename=None,  # The name of the file to save the PDF to. If None, the PDF is returned as a buffer.
    label_width=99 * mm,  # The width of each label on the sheet.
    label_height=34 * mm,  # The height of each label on the sheet.
    qr_width=30 * mm,  # The width of the QR code image itself.
    qr_height=30 * mm,  # The height of the QR code image itself.
    rows=8,  # The number of label rows on the sheet.
    cols=2,  # The number of label columns on the sheet.
    margin_top=13 * mm,  # The top margin of the sheet.
    margin_left=5 * mm,  # The left margin of the sheet.
    space_x=0 * mm,  # The horizontal space between QR codes (columns).
    space_y=0 * mm,  # The vertical space between QR codes (rows).
    hint_font_size=8,  # The font size of the hint text.
    start_at_label=1,  # The number of the first label on the sheet.
):
    """Generate a PDF with QR codes for the given messages."""
    # Create a PDF buffer
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    page_width, page_height = A4

    # Initial X and Y positions based on margins
    inital_x_pos = margin_left
    initial_y_pos = page_height - margin_top

    # Iterate through the messages and create QR codes
    message_iter = iter(messages.items())  # Create an iterator for the messages
    for label_number in range(start_at_label, rows * cols + start_at_label):
        try:
            hint, message = next(message_iter)
        except StopIteration:
            break  # Stop if there are no more messages

        # Calculate the position based on label number
        row = (label_number - 1) // cols
        col = (label_number - 1) % cols

        x_pos = inital_x_pos + (col * (label_width + space_x))
        y_pos = initial_y_pos - (row * (label_height + space_y)) % (
            page_height - margin_top
        )

        # Draw QR code on the PDF
        qr_img = generate_qr_code(message)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        c.drawImage(
            ImageReader(qr_buffer),
            x_pos,
            y_pos - label_height,
            width=qr_width,
            height=qr_height,
        )
        c.setFont("Helvetica", hint_font_size)
        c.drawString(x_pos + qr_width + 10 * mm, y_pos - 10 * mm, hint)

        # Add a new page if end of current page is reached
        if (
            label_number % (rows * cols) == 0
            and label_number < rows * cols + start_at_label - 1
        ):
            c.showPage()
            # Reset Y to initial position at the top of the next page
            initial_y_pos = page_height - margin_top

    c.save()

    # Move to the beginning of the BytesIO buffer
    pdf_buffer.seek(0)

    # Save or return the PDF
    if filename:
        with open(filename, "wb") as f:
            f.write(pdf_buffer.getvalue())
        return filename
    else:
        return pdf_buffer.getvalue()


"""
from core.labels import *

generate_pdf_for_qr_codes(messages, filename="media/test.pdf")
"""
messages = {
    "000": "http://127.0.0.1:8000/login/?next=/stock/24/",
    "111": "3iIyX;K\"_<hN2MLm@<l$Ya1~E#D9W0'[-:Y_z-YkOP&qdS\\!3m3T.mUXE~J1{OB)PCCxW7@7qVZJI}AlYZa[rzj6 ^-nBn$1N,8w",
    "222": ":& 3bH@6c``O#6mtr/viu|H$31gj-9jR3Aj2}#_x;[#Xm(/_<M8i/Cq<r)5karN@@+},OzAo)(c]{!SD_6*{f`_G+g7fk)h/nD:",
    "333": "%e%V?IfT 7wKOh6/O?-Q[b,M\\8^9S*ed\\_7WHHzX#XBAk-srQnsAe;|n`_qf&R3A02w[MWvgNS!cnpY*vxr~q%^,9YSDd\\fxl}p",
    "444": "041>n[7)Vv1rDo%@<e8|Z &9iK.2:B=^=e1Azv`5G%Y!Ev)uKrgOn[6'z 7r*,cT*w.p$g0;V\\l/DkuK^QZDoSK?sdCP^r]lY'/\"",
    "555": "#p{)zggmb068Fu&<Im@/tl]I/dAWF*U$iBI)mHu+0u_~Y_(d|fc]\\ 976;EI((l5t6|c}G<x=nNX8Myq>^ez)Cb)x$WQ&7:>xLGh",
    "666": "WfxJEU14+xGX^>8T?3,uT;)5XO^/QR|A7NRT6tV-HA|9-Ad*=N_(:fm~?yKNEJ%6|QgRYD-^bqgQ9|F27i@W3i8TFr!M[5)3V,D",
    "777": "http://127.0.0.1:8000/login/?next=/stock/29/",
    "888": "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "999": "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua lorem ipsum dolor sit amet, consectetur adipiscing elit, .",
    "AAA": "& 3bH@6c``O#6mtr/viu|H$31gj-9jR3Aj2}#_x;[#Xm(/_<M8i/Cq<r)5karN@@+},OzAo)(c]{!SD_6*{f`_G+g7fk)h/nD:",
    "BBB": "e%V?IfT 7wKOh6/O?-Q[b,M\\8^9S*ed\\_7WHHzX#XBAk-srQnsAe;|n`_qf&R3A02w[MWvgNS!cnpY*vxr~q%^,9YSDd\\fxl}p",
    "CCC": "WfxJEU14+xGX^>8T?3,uT;)5XO^/QR|A7NRT6tV-HA|9-Ad*=N_(:fm~?yKNEJ%6|QgRYD-^bqgQ9|F27i@W3i8TFr!M[5)3V,D",
    "DDD": "http://127.0.0.1:8000/login/?next=/stock/25/",
    "EEE": "lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "FFF": "ed do eiusmod tempor incididunt ut labore et dolore magna aliqua lorem ipsum dolor sit amet, consectetur adipiscing elit, .",
}
