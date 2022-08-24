import os
from PIL import Image


def convert_jpg_to_png(image_path):

    try:
        im = Image.open(image_path)
        imagePath = os.path.split(image_path)[-1][:-3] + 'png'
        imagePath = 'Images/Conversion/' + imagePath

        im.save(imagePath)
        return imagePath

    except:
        return False
