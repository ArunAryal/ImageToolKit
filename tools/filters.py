from PIL import Image, ImageEnhance
import numpy as np
import cv2

# Basic filters (PIL) 

def to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L").convert("RGB")  # keep 3 channels for consistency


def to_sepia(image: Image.Image) -> Image.Image:
    grayscale = image.convert("L")
    sepia = Image.merge("RGB", [
        grayscale.point(lambda p: min(p * 1.08, 255)),  # R
        grayscale.point(lambda p: min(p * 0.85, 255)),  # G
        grayscale.point(lambda p: min(p * 0.66, 255)),  # B
    ])
    return sepia


def invert_colors(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    arr = np.array(rgb)
    inverted = 255 - arr
    return Image.fromarray(inverted.astype(np.uint8))


#  Adjustments (PIL) 

def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """factor: 0.0 = black, 1.0 = original, 2.0 = double brightness"""
    return ImageEnhance.Brightness(image).enhance(factor)


def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    """factor: 0.0 = grey, 1.0 = original, 2.0 = high contrast"""
    return ImageEnhance.Contrast(image).enhance(factor)


def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
    """factor: 0.0 = blur, 1.0 = original, 2.0 = sharpened"""
    return ImageEnhance.Sharpness(image).enhance(factor)


def adjust_saturation(image: Image.Image, factor: float) -> Image.Image:
    """factor: 0.0 = grayscale, 1.0 = original, 2.0 = vivid"""
    return ImageEnhance.Color(image).enhance(factor)


#  Advanced filters (OpenCV) 

def _pil_to_cv(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)


def _cv_to_pil(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))

# Gaussian blur. intensity must be odd number.
def apply_blur(image: Image.Image, intensity: int) -> Image.Image:
    intensity = intensity if intensity % 2 == 1 else intensity + 1
    cv_img = _pil_to_cv(image)
    blurred = cv2.GaussianBlur(cv_img, (intensity, intensity), 0)
    return _cv_to_pil(blurred)


# Canny edge detection
def apply_edge_detection(image: Image.Image) -> Image.Image:
    cv_img = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(cv_img, 100, 200)
    return Image.fromarray(edges).convert("RGB")


# Unsharp mask sharpening via OpenCV
def apply_sharpen(image: Image.Image) -> Image.Image:
    cv_img = _pil_to_cv(image)
    blurred = cv2.GaussianBlur(cv_img, (0, 0), 3)
    sharpened = cv2.addWeighted(cv_img, 1.5, blurred, -0.5, 0)
    return _cv_to_pil(sharpened)