from PIL import Image
from utils.helpers import image_to_buffer
import io

SUPPORTED_FORMATS = ["JPEG", "PNG", "WEBP", "BMP", "TIFF"]

# Some formats don't support transparency (RGBA)
_FORMATS_NO_ALPHA = {"JPEG", "BMP"}

# Convert image to target format and return as BytesIO buffer.
def convert_image(image: Image.Image, target_fmt: str) -> io.BytesIO:
    converted = image.copy()

    # Strip alpha channel if target format doesn't support it
    if target_fmt.upper() in _FORMATS_NO_ALPHA and converted.mode == "RGBA":
        converted = converted.convert("RGB")

    return image_to_buffer(converted, fmt=target_fmt)


#Return the correct file extension for a given format.
def get_format_ext(fmt: str) -> str:
    return "jpg" if fmt.upper() == "JPEG" else fmt.lower()