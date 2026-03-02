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

elif tool == "resize":
    st.title("📐 Resize")
    if require_image():
        from tools.resize import(
            get_dimensions, resize_by_pixels,resize_by_percentage,
            resize_by_height,resize_by_width,image_to_buffer
        )

        image=st.session_state['image']
        filename=st.session_state['filename']
        base_name=filename.rsplit(".",1)[0]
        org_w,org_h=get_dimensions(image)

        col1,col2=st.columns(2)

        with col1:
            st.subheader("Original")
            st.image(image,use_container_width=True)
            st.caption(f"Current size: {org_w} * {org_h} px")
        
        with col2:
            st.subheader("Resize Options")
            mode=st.radio(
                "Resize by",
                ["Percentage","Exact Pixels","Fixed Width","Fixed Height"],
                horizontal=True
            )

            if mode=="Percentage":
                percent=st.slider("Scale %",min_value=1,max_value=300,value=100,step=1)
                new_w=int(org_w*percent/100)
                new_h=int(org_h*percent/100)
                st.caption(f"Output size:{new_w} * {new_h} px")
                resized=resize_by_percentage(image,percent)

            elif mode=="Exact Pixels":
                new_w=st.number_input("Width(px)",min_value=1,value=org_w)
                new_h=st.number_input("Height (px)",min_value=1,value=org_h)
                st.caption("⚠️ Aspect ratio not preserved")
                resized= resize_by_pixels(image,new_w,new_h)

            elif mode == "Fixed Width":
                new_w = st.number_input("Width (px)", min_value=1, value=org_w)
                ratio = new_w / org_w
                st.caption(f"Output size: {new_w} * {int(org_h * ratio)} px (aspect ratio preserved)")
                resized = resize_by_width(image, new_w)

            elif mode=="Fixed Height":
                new_h=st.number_input("Height (px)",min_value=1,value=org_h)
                ratio=new_h/org_h
                st.caption(f"Output size :{int(org_w * ratio )} * {new_h} px (aspect ratio preserved)")
                resized=resize_by_height(image,new_h)

            st. divider()
            st.subheader("Preview")
            st.image(resized,use_container_width=True)
            final_w,final_h =get_dimensions(resized)
            st.caption(f"New size: {final_w} * {final_h} px")

            buffer=image_to_buffer(resized,fmt="PNG")
            st.download_button(
                label="⬇️ Download Resized Image",
                data=buffer,
                file_name=f"resized_{base_name}.png",
                mime="image/png",
                type="primary"
            )
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
        from tools.metadata import get_metadata, classify_metadata,strip_metadata

        image=st.session_state['image']
        filename=st.session_state['filename']
        base_name=filename.rsplit(".",1)[0]

        col1,col2=st.columns(2)

        with col1:
            st.subheader("Preview")
            st.image(image,use_container_width=True)

        with col2:
            st.subheader("EXIF Metadata")
            metadata=get_metadata(image)

            if not metadata:
                st.success(" ✅ No EXIF metadata found in this image.")
            else:
                classified=classify_metadata(metadata)
                sensitive=classified["sensitive"]
                normal=classified['normal']

                if sensitive:
                    st.error(f"🚨 {len(sensitive)} sensitive field(s) found:")
                    for key,value in sensitive.items():
                        st.error(f"**{key}**: {value}")

                if normal:
                    with st.expander(f"View {len(normal)} other metadata fields"):
                        for key,value in normal.items():
                            st.text(f"{key}:{value}")
                st.divider()
                st.warning(f"Total: **{len(metadata)}** metadata fields detected.")

                if st.button("🧹 Strip All Metadata", type="primary"):
                    clean_buffer=strip_metadata(image)
                    st.success("✅ Metadata stripped successfully!")
                    st.download_button(
                        label="⬇️ Download Clean Image",
                        data=clean_buffer,
                        file_name=f"clean_{base_name}.png",
                        mime='image/png'
                    )

# elif tool=="grayscale"