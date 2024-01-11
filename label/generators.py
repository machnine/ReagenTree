""" label component generators """
from qrcode import constants, QRCode


class QRCodeImage:
    """Wrapper for a QR code image."""

    def __init__(self, image):
        self.image = image

    def save(self, filename):
        """Save the image to a file."""
        self.image.save(filename)


class QRCodeGenerator:
    """
    The QR code generator.
    'L' - About 7% or fewer errors can be corrected.
    'M' - About 15% or fewer errors can be corrected.
    'Q' - About 25% or fewer errors can be corrected.
    'H' - About 30% or fewer errors can be corrected.

    Default values:
     - version: None (auto, 1-40 different sizes)
     - error_correction: 'M'
     - box_size: 10
     - border: 4
     - fill_color: 'black'
     - back_color: 'white'
    """

    def __init__(self, **kwargs):
        self.CORRECTIONS = {
            "L": constants.ERROR_CORRECT_L,
            "M": constants.ERROR_CORRECT_M,
            "Q": constants.ERROR_CORRECT_Q,
            "H": constants.ERROR_CORRECT_H,
        }
        self.version = kwargs.get("version", None)
        self.error_correction = self.CORRECTIONS.get(
            kwargs.get("error_correction", "M"), constants.ERROR_CORRECT_M
        )
        self.box_size = kwargs.get("box_size", 10)
        self.border = kwargs.get("border", 4)
        self.fill_color = kwargs.get("fill_color", "black")
        self.back_color = kwargs.get("back_color", "white")

    def make(self, message) -> QRCodeImage:
        """Generate a QR code for the given message."""
        qr = QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(message)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
        return QRCodeImage(img)
