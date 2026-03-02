import streamlit as st
from PIL import Image
import io

# Page config
st.set_page_config(
    page_title="Image Toolkit",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

#slidebar
st.sidebar.title("🖼️ Image Toolkit")
st.sidebar.markdown("Your private, offline-first image editor")

TOOLS={
        "🏠 Home":        "home",
    "✂️  Crop":        "crop",
    "📐 Resize":      "resize",
    "🔄 Rotate/Flip": "rotate",
    "🗜️  Compress":    "compress",
    "🔁 Convert":     "convert",
    "🎨 Filters":     "filters",
    "🔍 Metadata":    "metadata",
}

selected=st.sidebar.radio("Select a Tool",list(TOOLS.keys()))
tool=TOOLS[selected]

st.sidebar.divider()
st.sidebar.caption("All processing happens locally Nothing is uploaded anywhere.")

# File Uploader
if tool!= 'home':
    uploaded_file=st.sidebar.file_uploader(
        "Upload an Image",
        type=["jpg","jpeg","png","webp","bmp","tiff"],
    )

    if uploaded_file:
        # store image in session state so tools can access it
        image=Image.open(uploaded_file)
        st.session_state["image"]=image
        st.session_state["filename"]=uploaded_file.name

# Show if no image is uploaded
def require_image():
    if "image" not in st.session_state:
        st.info("👈 Upload an image from the sidebar to get started")
        return False
    return True


#Pages

if tool=="home":
    st.title("Welcome to the Image Toolkit🖼️")
    st.markdown("""
    A **private, browser-based** image editor — no third-party servers, no data collection.

    ### What you can do:
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

elif tool=="crop":
    st.title("✂️ Crop")
    if require_image():
        st.image(st.session_state["image"],caption="Original Image",use_container_width=True)
        st.info("🚧 Crop tool coming next!")

elif tool=="rotate":
    st.title("🔄 Rotate / Flip")
    if require_image():
        st.image(st.session_state["image"],caption="Original Image",use_container_width=True)
        st.info("🚧 Rotate tool coming next!")

elif tool=="compress":
    st.title("🗜️ Compress")
    if require_image():
        st.image(st.session_state["image"],caption="Original Image",use_container_width=True)
        st.info("🚧 Compress tool coming next!")

elif tool=="convert":
    st.title("🔁 Convert")
    if require_image():
        st.image(st.session_state["image"],caption="Original Image",use_container_width=True)
        st.info("🚧 Convert tool coming next!")

elif tool=="filters":
    st.title("🎨 Filters")
    if require_image():
        st.image(st.session_state["image"],caption="Original Image",use_container_width=True)
        st.info("🚧 Filters tool coming next!")

elif tool=="metadata":
    st.title("🔍 Metadata")
    if require_image():
        st.image(st.session_state["image"],caption="Original Image",use_container_width=True)
        st.info("🚧 Metadata tool coming next!")