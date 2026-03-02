import cv2
from pathlib import Path

#load image
def load_image(image_path:str):
    img=cv2.imread(image_path)