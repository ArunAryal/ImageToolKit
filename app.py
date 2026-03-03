from __future__ import annotations
import streamlit as st
from PIL import Image

from utils.helpers import image_to_buffer
from utils.ui import (
    build_size_bars,
    get_image_context,
    render_download_button,
    require_image,
)
from tools.compress import (
    compress_image,
    get_compressed_size,
    get_original_size,
    bytes_to_kb,
    size_reduction_percent,
)
from tools.convert import convert_image, get_format_ext, SUPPORTED_FORMATS
from tools.filters import (
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    adjust_sharpness,
    apply_blur,
    apply_edge_detection,
    apply_sharpen,
    invert_colors,
    to_grayscale,
    to_sepia,
)
from tools.metadata import classify_metadata, get_metadata, strip_metadata
from tools.resize import (
    get_dimensions,
    resize_by_height,
    resize_by_percentage,
    resize_by_pixels,
    resize_by_width,
)
from tools.rotate import flip_horizontal, flip_vertical, rotate_image

#Page config 

st.set_page_config(
    page_title="Image Toolkit",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Sidebar 

TOOLS: dict[str, str] = {
    "🏠 Home":        "home",
    "✂️  Crop":        "crop",
    "📐 Resize":      "resize",
    "🔄 Rotate/Flip": "rotate",
    "🗜️  Compress":   "compress",
    "🔁 Convert":     "convert",
    "🎨 Filters":     "filters",
    "🔍 Metadata":    "metadata",
}

st.sidebar.title("🖼️ Image Toolkit")
st.sidebar.markdown("Your private, offline-first image editor")
selected = st.sidebar.radio("Select a Tool", list(TOOLS.keys()))
tool = TOOLS[selected]
st.sidebar.divider()
st.sidebar.caption("All processing happens locally. Nothing is uploaded anywhere.")

if tool != "home":
    uploaded_file = st.sidebar.file_uploader(
        "Upload an Image",
        type=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
    )
    if uploaded_file:
        if st.session_state.get("filename") != uploaded_file.name:
            # Reset per-image toggle state when a new file is loaded
            st.session_state["flip_horizontal"] = False
            st.session_state["flip_vertical"] = False
        st.session_state["image"] = Image.open(uploaded_file)
        st.session_state["filename"] = uploaded_file.name


#  Tool pages 

def render_home() -> None:
    st.title("Welcome to the Image Toolkit 🖼️")
    st.markdown("""
A **private, browser-based** image editor — no third-party servers, no data collection.

### What you can do
| Tool | Description |
|------|-------------|
| ✂️ Crop | Draw and crop any region |
| 📐 Resize | Resize by pixels or percentage |
| 🔄 Rotate/Flip | Rotate 90°/180° or flip horizontally/vertically |
| 🗜️ Compress | Reduce file size with quality control |
| 🔁 Convert | Convert between JPG, PNG, WEBP, BMP, TIFF |
| 🎨 Filters | Grayscale, blur, sharpen, brightness, contrast |
| 🔍 Metadata | View and strip EXIF data (GPS, device info, timestamps) |

**Get started** → Select a tool from the sidebar and upload an image.
""")


def render_crop() -> None:
    st.title("✂️ Crop")
    if not require_image():
        return

    from streamlit_cropper import st_cropper  # type: ignore[import]

    image, base_name, fmt, ext = get_image_context()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Select Crop Region")
        cropped = st_cropper(image, realtime_update=True, box_color="red", aspect_ratio=None)

    with col2:
        st.subheader("Preview")
        st.image(cropped, use_container_width=True)
        w, h = cropped.size
        st.caption(f"Cropped size: {w} × {h} px")
        render_download_button(
            buffer=image_to_buffer(cropped, fmt=fmt),
            filename=f"cropped_{base_name}.{ext}",
            ext=ext,
            label="⬇️ Download Cropped Image",
        )


def render_rotate() -> None:
    st.title("🔄 Rotate / Flip")
    if not require_image():
        return

    image, base_name, fmt, ext = get_image_context()

    st.session_state.setdefault("flip_horizontal", False)
    st.session_state.setdefault("flip_vertical", False)

    result = image
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rotate")
        angle = st.select_slider("Angle", options=[0, 90, 180, 270], value=0)
        if angle:
            result = rotate_image(result, angle)

        st.subheader("Flip")
        col_h, col_v = st.columns(2)

        with col_h:
            h_label = "✅ Horizontal" if st.session_state["flip_horizontal"] else "↔️ Horizontal"
            if st.button(h_label, use_container_width=True):
                st.session_state["flip_horizontal"] = not st.session_state["flip_horizontal"]
                st.rerun()

        with col_v:
            v_label = "✅ Vertical" if st.session_state["flip_vertical"] else "↕️ Vertical"
            if st.button(v_label, use_container_width=True):
                st.session_state["flip_vertical"] = not st.session_state["flip_vertical"]
                st.rerun()

        if st.session_state["flip_horizontal"]:
            result = flip_horizontal(result)
        if st.session_state["flip_vertical"]:
            result = flip_vertical(result)

    with col2:
        st.subheader("Preview")
        st.image(result, use_container_width=True)
        w, h = result.size
        st.caption(f"Output size: {w} × {h} px")
        st.divider()
        render_download_button(
            buffer=image_to_buffer(result, fmt=fmt),
            filename=f"rotated_{base_name}.{ext}",
            ext=ext,
            label="⬇️ Download Image",
        )


def render_compress() -> None:
    st.title("🗜️ Compress")
    if not require_image():
        return

    image, base_name, _fmt, _ext = get_image_context()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Compression Settings")
        quality_percent = st.slider(
            "Quality %",
            min_value=10,
            max_value=100,
            value=85,
            step=5,
            help="100% = original quality. Lower = smaller file, more artifacts.",
        )

        original_size = get_original_size(image)
        compressed_size = get_compressed_size(image, quality_percent)
        original_kb = bytes_to_kb(original_size)
        compressed_kb = bytes_to_kb(compressed_size)
        reduction = size_reduction_percent(original_size, compressed_size)

        st.divider()
        st.subheader("📊 Size Comparison")
        st.markdown(build_size_bars(original_kb, compressed_kb), unsafe_allow_html=True)
        st.caption(f"**{reduction}% smaller** — {original_kb} KB → {compressed_kb} KB")
        st.divider()

        if quality_percent >= 80:
            st.success("✅ High quality — minimal visible difference")
        elif quality_percent >= 50:
            st.warning("⚠️ Medium quality — some loss on close inspection")
        else:
            st.error("🚨 Low quality — visible compression artifacts")

        render_download_button(
            buffer=compress_image(image, quality_percent),
            filename=f"compressed_{base_name}.jpg",
            ext="jpg",
            label="⬇️ Download Compressed Image",
        )


def render_resize() -> None:
    st.title("📐 Resize")
    if not require_image():
        return

    image, base_name, fmt, ext = get_image_context()
    org_w, org_h = get_dimensions(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)
        st.caption(f"Current size: {org_w} × {org_h} px")

    with col2:
        st.subheader("Resize Options")
        mode = st.radio(
            "Resize by",
            ["Percentage", "Exact Pixels", "Fixed Width", "Fixed Height"],
            horizontal=True,
        )

        if mode == "Percentage":
            percent = st.slider("Scale %", min_value=1, max_value=300, value=100, step=1)
            new_w, new_h = int(org_w * percent / 100), int(org_h * percent / 100)
            st.caption(f"Output size: {new_w} × {new_h} px")
            resized = resize_by_percentage(image, percent)

        elif mode == "Exact Pixels":
            new_w = st.number_input("Width (px)", min_value=1, value=org_w)
            new_h = st.number_input("Height (px)", min_value=1, value=org_h)
            st.caption("⚠️ Aspect ratio not preserved")
            resized = resize_by_pixels(image, int(new_w), int(new_h))

        elif mode == "Fixed Width":
            new_w = st.number_input("Width (px)", min_value=1, value=org_w)
            st.caption(
                f"Output size: {int(new_w)} × {int(org_h * new_w / org_w)} px"
                " (aspect ratio preserved)"
            )
            resized = resize_by_width(image, int(new_w))

        else:  # Fixed Height
            new_h = st.number_input("Height (px)", min_value=1, value=org_h)
            st.caption(
                f"Output size: {int(org_w * new_h / org_h)} × {int(new_h)} px"
                " (aspect ratio preserved)"
            )
            resized = resize_by_height(image, int(new_h))

        st.divider()
        render_download_button(
            buffer=image_to_buffer(resized, fmt=fmt),
            filename=f"resized_{base_name}.{ext}",
            ext=ext,
            label="⬇️ Download Resized Image",
        )


def render_convert() -> None:
    st.title("🔁 Convert")
    if not require_image():
        return

    image, base_name, current_fmt, _ext = get_image_context()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(image, use_container_width=True)
        st.caption(f"Current format: **{current_fmt}**  |  Mode: **{image.mode}**")

    with col2:
        st.subheader("Convert To")
        options = [f for f in SUPPORTED_FORMATS if f != current_fmt]
        target_fmt = st.selectbox("Target Format", options)

        if image.mode == "RGBA" and target_fmt in ("JPEG", "BMP"):
            st.warning("⚠️ JPEG and BMP don't support transparency. Alpha channel will be removed.")

        st.divider()
        ext = get_format_ext(target_fmt)
        st.success(f"✅ Ready to download as **{target_fmt}**")
        render_download_button(
            buffer=convert_image(image, target_fmt),
            filename=f"{base_name}.{ext}",
            ext=ext,
            label=f"⬇️ Download as {target_fmt}",
        )


def render_filters() -> None:
    st.title("🎨 Filters")
    if not require_image():
        return

    image, base_name, fmt, ext = get_image_context()
    result = image.copy()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎨 Color Filters")
        color_filter = st.radio(
            "Apply Filter",
            ["None", "Grayscale", "Sepia", "Invert"],
            horizontal=True,
        )
        if color_filter == "Grayscale":
            result = to_grayscale(result)
        elif color_filter == "Sepia":
            result = to_sepia(result)
        elif color_filter == "Invert":
            result = invert_colors(result)

        st.divider()
        st.subheader("⚙️ Adjustments")
        brightness = st.slider("Brightness", 0.0, 2.0, 1.0, step=0.05)
        contrast   = st.slider("Contrast",   0.0, 2.0, 1.0, step=0.05)
        saturation = st.slider("Saturation", 0.0, 2.0, 1.0, step=0.05)
        sharpness  = st.slider("Sharpness",  0.0, 2.0, 1.0, step=0.05)

        if brightness != 1.0:
            result = adjust_brightness(result, brightness)
        if contrast != 1.0:
            result = adjust_contrast(result, contrast)
        if saturation != 1.0:
            result = adjust_saturation(result, saturation)
        if sharpness != 1.0:
            result = adjust_sharpness(result, sharpness)

        st.divider()
        st.subheader("🔬 Advanced")
        advanced = st.radio(
            "Apply Effect",
            ["None", "Blur", "Sharpen", "Edge Detection"],
            horizontal=True,
        )
        if advanced == "Blur":
            blur_intensity = st.slider("Blur Intensity", 1, 21, 5, step=2)
            result = apply_blur(result, blur_intensity)
        elif advanced == "Sharpen":
            result = apply_sharpen(result)
        elif advanced == "Edge Detection":
            result = apply_edge_detection(result)

    with col2:
        st.subheader("Preview")
        st.image(result, use_container_width=True)
        st.divider()
        render_download_button(
            buffer=image_to_buffer(result, fmt=fmt),
            filename=f"filtered_{base_name}.{ext}",
            ext=ext,
            label="⬇️ Download Filtered Image",
        )


def render_metadata() -> None:
    st.title("🔍 Metadata")
    if not require_image():
        return

    image, base_name, _fmt, _ext = get_image_context()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Preview")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("EXIF Metadata")
        metadata = get_metadata(image)

        if not metadata:
            st.success("✅ No EXIF metadata found in this image.")
            return

        classified = classify_metadata(metadata)
        sensitive = classified["sensitive"]
        normal = classified["normal"]

        if sensitive:
            st.error(f"🚨 {len(sensitive)} sensitive field(s) found:")
            for key, value in sensitive.items():
                st.error(f"**{key}**: {value}")

        if normal:
            with st.expander(f"View {len(normal)} other metadata fields"):
                for key, value in normal.items():
                    st.text(f"{key}: {value}")

        st.divider()
        st.warning(f"Total: **{len(metadata)}** metadata fields detected.")

        if st.button("🧹 Strip All Metadata", type="primary"):
            clean_buffer = strip_metadata(image)
            st.success("✅ Metadata stripped successfully!")
            st.download_button(
                label="⬇️ Download Clean Image",
                data=clean_buffer,
                file_name=f"clean_{base_name}.png",
                mime="image/png",
            )


# Dispatch table 

_RENDERERS = {
    "home":     render_home,
    "crop":     render_crop,
    "rotate":   render_rotate,
    "compress": render_compress,
    "resize":   render_resize,
    "convert":  render_convert,
    "filters":  render_filters,
    "metadata": render_metadata,
}

_RENDERERS[tool]()