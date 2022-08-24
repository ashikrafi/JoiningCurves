# import numpy
# import pytoshop
# from PIL import Image
# from pytoshop.user import nested_layers
# from pytoshop import enums
# from pytoshop.image_data import ImageData
#
# tga='Images/Input/NR_001.jpg'
# im = Image.open(tga)
# print(im)
# layers = []
# arr = numpy.array(im)
# channels = [arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]]
# data = ImageData(channels=numpy.array(im))
# newLayer = nested_layers.Image(name=tga.replace(".tga", ""), visible=True, opacity=255, group_id=0,
#                                blend_mode=enums.BlendMode.normal, top=0,
#                                left=0, channels=channels,
#                                metadata=None, layer_color=0, color_mode=None)
# layers.append(newLayer)
# output = nested_layers.nested_layers_to_psd(layers, color_mode=3, size=(1024, 1024))
# print(newLayer)

import numpy
from PIL import Image
from pytoshop.user import nested_layers
from pytoshop import enums
from pytoshop.image_data import ImageData
import os
import pytoshop

cwd = '/home/kow/PycharmProjects/IBR/Images/Input/'
tgas = [x for x in os.listdir(cwd)]


layers = []
for tga in tgas:
    im = Image.open(cwd + tga)
    arr = numpy.array(im)
    channels = [arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]]

    data = ImageData(channels=numpy.array(im))
    newLayer = nested_layers.Image(name=tga.replace(".jpg", ""), visible=True, opacity=255, group_id=0,
                                   blend_mode=enums.BlendMode.normal, top=0,
                                   left=0, bottom=im.height, right=im.width, channels=channels,
                                   metadata=None, layer_color=7, color_mode=None)
    # print(im.getdata().mode)
    layers.append(newLayer)

# output = nested_layers.nested_layers_to_psd(layers, color_mode=3, size=(1024, 1024))
output = nested_layers.nested_layers_to_psd(layers, color_mode=3)

with open('updated.psd', 'wb') as fd:
    output.write(fd)

