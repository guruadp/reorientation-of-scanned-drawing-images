import cv2
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import math
import pytesseract
import re
import glob

from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
    )

kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))

def pdf_to_image(file):

    name = file.split('.')[0]
    images = convert_from_path(file)
    for i, image in enumerate(images):
        fname = str(name) + '.jpg'
        image.save(fname, "JPEG")
    return fname

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def angle_detection_hough_line(image):
    image = cv2.imread(image)
    image = rescaleFrame(image, 0.5)
    #image1 = Image.fromarray(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    cv2.imshow('Threshold', binary)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel1)
    edges = cv2.Canny(opening, 50, 150, apertureSize=3)
    cv2.imshow('Edges', edges)
    angles = []
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lines = cv2.HoughLines(binary, 1, np.pi / 180, 400)
    for line in lines:
        rho, theta = line[0]
        theta = float((theta * 180) / math.pi)
        angles.append(round(theta, 3))

    count = {i: angles.count(i) for i in angles}
    hough_angle = list(count.keys())[list(count.values()).index(max(count.values()))]
    return hough_angle

def hough_rotation(image,angle):
    image = cv2.imread(image)
    image1 = Image.fromarray(image)

    if (angle == 45) or (angle == 135) or (angle == 225) or (angle == 315):
        rotated_image = image1.rotate(45, fillcolor="white", expand=True)

    elif (angle > 0) and (angle < 45):
        rotated_image = image1.rotate(angle, fillcolor="white", expand=True)

    elif (angle > 45) and (angle < 135):
        rotated_image = image1.rotate(angle - 90, fillcolor="white", expand=True)

    elif (angle > 135) and (angle < 225):
        rotated_image = image1.rotate(angle - 180, fillcolor="white", expand=True)

    elif (angle > 225) and (angle < 315):
        rotated_image = image1.rotate(angle - 270, fillcolor="white", expand=True)

    else:
        rotated_image = image1.rotate(angle - 360, fillcolor="white", expand=True)

    rotated_image = np.array(rotated_image)

    return rotated_image

def ocr_rotation(image):
    image1 = Image.fromarray(image)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    try:
        osd = pytesseract.image_to_osd(gray)
        angle = re.search('(?<=Rotate: )\d+', osd).group(0)
        angle = float(angle)
        if angle > 0:
            angle = 360 - angle

    except:
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        osd = pytesseract.image_to_osd(edges)
       
        angle = re.search('(?<=Rotate: )\d+', osd).group(0)
        angle = float(angle)
        if angle > 0:
            angle = 360 - angle
    

    rotated_image = image1.rotate(angle, fillcolor="white", expand=True)
    rotated_image = np.array(rotated_image)
    return rotated_image


def save_file(filename, img_rotated):
    filename = str(filename.split(".")[0]) + "_rotated.png"
    cv2.imwrite(filename, img_rotated)

file = "1.pdf"
image = pdf_to_image(file)
hough_angle = angle_detection_hough_line(image)
if (hough_angle == 0) or (hough_angle == 90) or (hough_angle == 180) or (hough_angle == 360):
    image = cv2.imread(image)
    rotated_image = ocr_rotation(image)
else:
    rotated_image = hough_rotation(image, hough_angle)
    rotated_image = ocr_rotation(rotated_image)

print(hough_angle)
save_file(file, rotated_image)
cv2.waitKey(0)