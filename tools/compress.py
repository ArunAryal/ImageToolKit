from PIL import Image
from utils.helpers import image_to_buffer
import io


def quality_from_percent(percent: int) -> int:
    """
    Map a user-facing percentage (10-100) to a JPEG quality value (1-95).
    100% quality → 95 (PIL max), 10% quality → 1
    """
    return max(1, min(95, int(percent * 0.95)))


def compress_image(image: Image.Image, percent: int) -> io.BytesIO:
    """Compress image at given quality percentage. Always outputs JPEG."""
    quality = quality_from_percent(percent)
    rgb = image.convert("RGB")
    buffer = io.BytesIO()
    rgb.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer


def get_compressed_size(image: Image.Image, percent: int) -> int:
    """Return predicted compressed size in bytes."""
    buffer = compress_image(image, percent)
    return buffer.getbuffer().nbytes


def get_original_size(image: Image.Image) -> int:
    """Return original image size in bytes."""
    buffer = image_to_buffer(image, fmt=image.format or "PNG")
    return buffer.getbuffer().nbytes


def bytes_to_kb(size_bytes: int) -> float:
    return round(size_bytes / 1024, 2)


def size_reduction_percent(original: int, compressed: int) -> float:
    if original == 0:
        return 0.0
    return round((1 - compressed / original) * 100, 1)


def build_bar(label: str, size_kb: float, max_kb: float, color: str) -> str:
    """
    Build an HTML progress bar for size visualization.
    Width is proportional to size relative to max_kb.
    """
    width = max(2, int((size_kb / max_kb) * 100)) if max_kb > 0 else 0
    return f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="font-size: 14px; font-weight: 500;">{label}</span>
            <span style="font-size: 14px; color: #888;">{size_kb} KB</span>
        </div>
        <div style="background: #2a2a2a; border-radius: 6px; height: 20px; width: 100%;">
            <div style="
                background: {color};
                width: {width}%;
                height: 20px;
                border-radius: 6px;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """