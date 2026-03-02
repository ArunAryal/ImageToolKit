from PIL import Image
import io

try:
    from PIL import ImageResampling
    RESAMPLE = ImageResampling.LANCZOS
except ImportError:
    # Fallback for Pillow < 10
    RESAMPLE = Image.LANCZOS


def get_dimentions(image:Image.Image)->tuple[int,int]:
    return image.size

def resize_by_pixels(image:Image.Image,width:int,height:int)->Image.Image:
    return image.resize((width,height),RESAMPLE)

def resize_by_percentage(image:Image.Image,percent:float)-> Image.Image:
    org_w,org_h=image.size
    new_w=int(org_w*percent/100)
    new_h=int(org_h*percent/100)
    return image.resize((new_w,new_h),RESAMPLE)

def resize_by_width(image: Image.Image, width: int) -> Image.Image:
    orig_w, orig_h = image.size
    ratio = width / orig_w
    height = int(orig_h * ratio)
    return image.resize((width, height), RESAMPLE)

def resize_by_height(image: Image.Image, height: int) -> Image.Image:
    orig_w, orig_h = image.size
    ratio = height / orig_h
    width = int(orig_w * ratio)
    return image.resize((width, height), RESAMPLE)

def image_to_buffer(image: Image.Image, fmt: str = "PNG") -> io.BytesIO:
    buffer = io.BytesIO()
    image.save(buffer, format=fmt)
    buffer.seek(0)
    return buffer