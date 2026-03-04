# 🖼️ Image Toolkit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://imagetoolkit.streamlit.app)


A private, offline-first image editor built with Streamlit. All processing happens locally — no data is uploaded anywhere.

---

## Features

| Tool | Description |
|------|-------------|
| ✂️ Crop | Draw and crop any region |
| 📐 Resize | Resize by percentage, exact pixels, fixed width, or fixed height |
| 🔄 Rotate / Flip | Rotate 90°/180°/270° or flip horizontally/vertically |
| 🗜️ Compress | Reduce file size with quality control and live size preview |
| 🔁 Convert | Convert between JPG, PNG, WEBP, BMP, TIFF |
| 🎨 Filters | Grayscale, sepia, invert, brightness, contrast, saturation, blur, sharpen, edge detection |
| 🔍 Metadata | View and strip EXIF data (GPS, device info, timestamps) |

---

## Project Structure

```
image-toolkit/
├── app.py                  # Streamlit entry point
├── tools/
│   ├── compress.py
│   ├── convert.py
│   ├── crop.py
│   ├── filters.py
│   ├── metadata.py
│   ├── resize.py
│   └── rotate.py
├── utils/
│   ├── helpers.py          # I/O utilities
│   └── ui.py               # Shared Streamlit UI helpers
├── pyproject.toml
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Install with uv

```bash
git clone https://github.com/ArunAryal/ImageToolKit.git
cd ImageToolKit
uv sync
```

### Install with pip

```bash
git clone https://github.com/ArunAryal/ImageToolKit.git
cd ImageToolKit
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Supported Formats

Input: `JPG`, `JPEG`, `PNG`, `WEBP`, `BMP`, `TIFF`

Output format depends on the tool — compress always outputs JPEG, all other tools preserve the original format unless you use Convert.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | UI framework |
| `Pillow` | Core image processing |
| `numpy` | Pixel-level operations (invert, sepia) |
| `opencv-python-headless` | Blur, sharpen, edge detection |
| `streamlit-cropper` | Interactive crop UI |

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.