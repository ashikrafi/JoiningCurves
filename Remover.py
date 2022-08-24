import io
import os
import numpy
import numpy as np
from PIL import Image
from PIL import ImageFile
from pytoshop import enums
from pytoshop.image_data import ImageData
from pytoshop.user import nested_layers

from FormatConversion import convert_jpg_to_png
from ImageMasking import remove


def process_image(iPath, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage):
    input_path = convert_jpg_to_png(iPath)

    if input_path:
        # format_conversion(input_path)
        f = np.fromfile(input_path)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        result = remove(f, input_path, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage)

        # image_name = str(get_image_name(input_path))
        #
        # image_name_without_ext = get_image_name_without_extension(input_path)
        # actual_output_path = 'Images/Output/Original/' + image_name
        # psd_output_path = 'Images/Output/PSD/' + image_name_without_ext + '.psd'
        #
        # img = Image.open(io.BytesIO(result)).convert("RGBA")
        # img.save(actual_output_path)
        # format_conversion(input_path, actual_output_path, psd_output_path)

        # auto_canny(img)


def convert_to_layers(imagePathLayers, PSDOutputPath):
    layers = []
    names = ['Original', 'Background Removal']
    counter = 0
    for tga in imagePathLayers:
        im = Image.open(tga)
        arr = numpy.array(im)
        channels = [arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]]

        data = ImageData(channels=numpy.array(im))
        newLayer = nested_layers.Image(name=names[counter], visible=True, opacity=255, group_id=0,
                                       blend_mode=enums.BlendMode.normal, top=0,
                                       left=0, bottom=im.height, right=im.width, channels=channels,
                                       metadata=None, layer_color=0, color_mode=None)
        # print(im.getdata().mode)
        counter = counter + 1
        layers.append(newLayer)

    # output = nested_layers.nested_layers_to_psd(layers, color_mode=3, size=(1024, 1024))
    output = nested_layers.nested_layers_to_psd(layers, color_mode=3)

    with open(PSDOutputPath, 'wb') as fd:
        output.write(fd)


def get_image_name(image_path):
    image_name = os.path.split(image_path)[-1]
    return image_name


def get_image_name_without_extension(image_path):
    base = os.path.basename(image_path)
    os.path.splitext(base)
    imageName = os.path.splitext(base)[0]
    return imageName


def format_conversion(input_path, actual_output_path, psd_output_path):
    pathLayers = [input_path, actual_output_path]
    convert_to_layers(pathLayers, psd_output_path)
