from PIL import Image
import io

def image_to_buffer(image:Image.Image,fmt:str=None)-> io.BytesIO:
    fmt =fmt or image.format or "PNG"

    if fmt.upper() in ("JPEG","JPG") and image.mode=="RGBA":
        image=image.convert("RGB")

    buffer=io.BytesIO()
    image.save(buffer,format=fmt)
    buffer.seek(0)
    return buffer