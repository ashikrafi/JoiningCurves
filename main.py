import datetime
import os
from Remover import process_image
import time
import sys


def load_images_from_folder_or_database(folder, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage):
    toolbar_width = get_number_of_images(folder)

    print("--------------------------------------")
    print("Total Number of Images in Folder: " + str(toolbar_width))
    print("--------------------------------------")
    print("Image Processing Started: " + str(datetime.datetime.now()))
    print("--------------------------------------")

    counter = 1
    sys.stdout.write("[-%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))

    for filename in os.listdir(folder):
        img = os.path.join(folder, filename)
        if img is not None:
            process_image(img, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage)
            line = str(counter) + '-'
            sys.stdout.write(line)
            sys.stdout.flush()
            counter = counter + 1

    sys.stdout.write("]\n")
    print("--------------------------------------")
    print("Image Processing Finished: " + str(datetime.datetime.now()))
    print("--------------------------------------")


def get_number_of_images(dir):
    list = os.listdir(dir)
    number_files = len(list)
    return number_files


if __name__ == '__main__':
    # # Fixed Margin from All Sides
    # MarginalVal = 20
    # leftMargin = rightMargin = topMargin = bottomMargin = MarginalVal

    # # Customized Margin
    leftMargin = 0
    rightMargin = 0
    topMargin = 0
    bottomMargin = 0

    IsPercentage = True

    load_images_from_folder_or_database('Images/Input/', leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage)
