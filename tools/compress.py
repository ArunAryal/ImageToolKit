# Image compression utilities
from PIL import Image
import io

from utils.helpers import image_to_buffer


def quality_from_percent(percent: int) -> int:
    # Map a user-facing percentage (10–100) to a JPEG quality value (1–95).
    return max(1, min(95, int(percent * 0.95)))


def compress_image(image: Image.Image, percent: int) -> io.BytesIO:
    # Compress *image* at *percent* quality and return a JPEG buffer
    quality = quality_from_percent(percent)
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer


def get_compressed_size(image: Image.Image, percent: int) -> int:
    # Return the predicted compressed size in bytes.
    return compress_image(image, percent).getbuffer().nbytes


def get_original_size(image: Image.Image) -> int:
    # Return the original image size in bytes
    return image_to_buffer(image, fmt=image.format or "PNG").getbuffer().nbytes


def bytes_to_kb(size_bytes: int) -> float:
    return round(size_bytes / 1024, 2)


def size_reduction_percent(original: int, compressed: int) -> float:
    if original == 0:
        return 0.0
    return round((1 - compressed / original) * 100, 1)