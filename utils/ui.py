# Shared Streamlit UI helpers used across tool pages.
from __future__ import annotations
import io
import streamlit as st
from PIL import Image
from utils.helpers import image_to_buffer


# Return ``True`` if an image is loaded in session state.Renders an informational prompt and returns ``False`` otherwise
def require_image() -> bool:
    if "image" not in st.session_state:
        st.info("👈 Upload an image from the sidebar to get started.")
        return False
    return True



# Unpack the current image and its derived metadata from session state.
def get_image_context() -> tuple[Image.Image, str, str, str]:
    image: Image.Image = st.session_state["image"]
    filename: str = st.session_state["filename"]
    base_name = filename.rsplit(".", 1)[0]
    fmt = (image.format or "PNG").upper()
    ext = "jpg" if fmt == "JPEG" else fmt.lower()
    return image, base_name, fmt, ext


# Render a primary-styled Streamlit download button.
def render_download_button(
    buffer: io.BytesIO,
    filename: str,
    ext: str,
    label: str = "⬇️ Download",
) -> None:
    mime = "image/jpeg" if ext == "jpg" else f"image/{ext}"
    st.download_button(
        label=label,
        data=buffer,
        file_name=filename,
        mime=mime,
        type="primary",
    )


# Return an HTML snippet with two proportional size-comparison bars.
def build_size_bars(original_kb: float, compressed_kb: float) -> str:
    def _bar(label: str, size_kb: float, max_kb: float, color: str) -> str:
        width = max(2, int((size_kb / max_kb) * 100)) if max_kb > 0 else 0
        return f"""
        <div style="margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:14px;font-weight:500;">{label}</span>
                <span style="font-size:14px;color:#888;">{size_kb} KB</span>
            </div>
            <div style="background:#2a2a2a;border-radius:6px;height:20px;width:100%;">
                <div style="background:{color};width:{width}%;height:20px;border-radius:6px;
                            transition:width 0.3s ease;"></div>
            </div>
        </div>"""

    return _bar("Original", original_kb, original_kb, "#4a9eff") + _bar(
        "Compressed", compressed_kb, original_kb, "#22c55e"
    )