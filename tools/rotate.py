from PIL import Image

def rotate_image(image:Image.Image,degrees:int)-> Image.Image:
    return image.rotate(degrees,expand=True)

def flip_horizontal(image:Image.Image)->Image.Image:
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(image:Image.Image)->Image.Image:
    return image.transpose(Image.FLIP_TOP_BOTTOM)