from PIL import Image

def crop_image(image:Image.Image,left:int,top:int,right:int,bottom:int) -> Image.Image:
    return image.crop((left,top,right,bottom))
