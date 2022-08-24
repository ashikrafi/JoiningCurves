import os
from PIL import Image, ImageFile
import imutils
import cv2

finalval = []


def get_image_name(image_path):
    image_name = os.path.split(image_path)[-1]
    return image_name


def image_resize(ImagePath, minXValue, maxXValue, minYValue, maxYValue, leftMargin, rightMargin, topMargin,
                 bottomMargin, IsPercentage):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    original = Image.open(ImagePath)

    width, height = original.size
    xRefVal = width - maxXValue
    yRefVal = height - maxYValue

    finalval.append(minXValue)
    finalval.append(minYValue)
    finalval.append(xRefVal)
    finalval.append(yRefVal)

    minRafVal = int(min(finalval))

    if not IsPercentage:
        left = int(minXValue) - leftMargin
        top = int(minYValue) - topMargin
        right = int(maxXValue) + rightMargin
        bottom = int(maxYValue) + bottomMargin

    else:
        # left = int(minXValue) - (int(minXValue) * leftMargin / 100)
        # top = int(minYValue) - (int(minYValue) * topMargin / 100)
        # right = int(maxXValue) + (rightMargin*2)
        # bottom = int(maxYValue) + (bottomMargin*2)

        # main
        # left = int(minXValue) - (int(minXValue) * leftMargin / 100)
        # top = int(minYValue) - (int(minYValue) * topMargin / 100)
        # right = int(maxXValue) + (int(maxXValue) * rightMargin / 100)
        # bottom = int(maxYValue) + (int(maxYValue) * bottomMargin / 100)

        # Test_Case
        # left = int(minXValue) - (int(minXValue) * leftMargin / 100)
        # top = int(minYValue) - (int(minYValue) * topMargin / 100)
        # right = int(maxXValue) + (int(maxXValue) * rightMargin / 100)
        # bottom = int(maxYValue) + (int(maxYValue) * bottomMargin / 100)

        if minXValue >= (width - maxXValue):
            # refVal = width - maxXValue
            refVal = minRafVal
            marginVal = (refVal * leftMargin / 100)
            left = int(minXValue) - marginVal
            right = int(maxXValue) + marginVal

        if minXValue < (width - maxXValue):
            # refVal = minXValue
            refVal = minRafVal
            marginVal = (refVal * rightMargin / 100)
            left = int(minXValue) - marginVal
            right = int(maxXValue) + marginVal

        if minYValue >= (height - maxYValue):
            # refVal = height - maxYValue
            refVal = minRafVal
            marginVal = (refVal * bottomMargin / 100)
            top = int(minYValue) - marginVal
            bottom = int(maxYValue) + marginVal

        if minYValue < (height - maxYValue):
            # refVal = minYValue
            refVal = minRafVal
            marginVal = (refVal * topMargin / 100)
            top = int(minYValue) - marginVal
            bottom = int(maxYValue) + marginVal

    cropped_example = original.crop((left, top, right, bottom)).convert("RGBA")
    image_name = str(get_image_name(ImagePath))
    print(cropped_example.size)
    cropped_example.save('Images/Output/' + image_name)


def GetImageContour(MaskImagePath, OriginalImagePath, leftMargin, rightMargin, topMargin, bottomMargin, IsPercentage):
    image = cv2.imread(MaskImagePath)
    xAxis = []
    yAxis = []

    height, width, channel = image.shape

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    xAxis.append(extLeft[0])
    xAxis.append(extRight[0])
    xAxis.append(extTop[0])
    xAxis.append(extBot[0])

    yAxis.append(extLeft[1])
    yAxis.append(extRight[1])
    yAxis.append(extTop[1])
    yAxis.append(extBot[1])

    minXValue = min(xAxis)
    maxXValue = max(xAxis)

    minYValue = min(yAxis)
    maxYValue = max(yAxis)

    image_resize(OriginalImagePath, minXValue, maxXValue, minYValue, maxYValue, leftMargin, rightMargin, topMargin,
                 bottomMargin, IsPercentage)
    # print(minXValue)
    # print(minYValue)
