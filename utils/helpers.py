# Low-level I/O helpers shared across the toolkit
from PIL import Image
import io

# Formats that cannot represent an alpha channel
_NO_ALPHA_FORMATS = {"JPEG", "JPG", "BMP"}


def image_to_buffer(image: Image.Image, fmt: str = "PNG") -> io.BytesIO:
    fmt = (fmt or image.format or "PNG").upper()
    save_fmt = "JPEG" if fmt == "JPG" else fmt

    if save_fmt in _NO_ALPHA_FORMATS and image.mode == "RGBA":
        image = image.convert("RGB")

    buffer = io.BytesIO()
    image.save(buffer, format=save_fmt)
    buffer.seek(0)
    return buffer