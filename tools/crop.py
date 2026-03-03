from PIL import Image
import io

def crop_image(image:Image.Image,left:int,top:int,right:int,bottom:int) -> Image.Image:
    return image.crop((left,top,right,bottom))
