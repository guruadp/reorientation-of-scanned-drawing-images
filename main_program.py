import cv2
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
import math
import pytesseract
import re
import glob
import imutils

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
    )

def pdf_to_image(file):
    name = file.split('.')[0]
    images = convert_from_path(file)
    for image in images:
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
    # cv2.imshow('Image', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   
    # cv2.imshow('Gray Image', gray) 
    _,binary = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    # cv2.imshow('Threshold', binary)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel1)
    # cv2.imshow('Opening', opening)
    canny = cv2.Canny(binary, 50, 150, apertureSize=3)    
    # cv2.imshow('Canny Edge', canny)
    angles = []     
    lines = cv2.HoughLinesP(
            canny, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=100, # Min number of votes for valid line
            minLineLength=250, # Min allowed length of line
            maxLineGap=20 # Max allowed gap between line for joining them
            )

    for points in lines:
        x1,y1,x2,y2=points[0]
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
        angle = math.atan2(y2 - y1, x2 - x1) 
        angle = round(math.degrees(angle), 1)
        # angle = angle if (angle>0) else angle + 90
        angles.append(angle)
    
    #cv2.imshow('Lines', image)
    count = {i: angles.count(i) for i in angles}
    hough_angle = list(count.keys())[list(count.values()).index(max(count.values()))]
    return hough_angle

def save_file(filename, img_rotated):
    filename = str(filename.split(".")[0]) + "_rotated.png"
    cv2.imwrite(filename, img_rotated)

file = "sample.pdf"
image = pdf_to_image(file)
hough_angle = angle_detection_hough_line(image)
print(f'Hough angle = {hough_angle}')

image = cv2.imread(image)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_osd(file.split('.')[0]+'.jpg')
# display the orientation information
ocr_angle = re.search('(?<=Orientation in degrees: )\d+', results).group(0)

ocr_angle = float(ocr_angle)
print(f'OCR angle = {ocr_angle}')
rotated = imutils.rotate_bound(image, angle=ocr_angle)
cv2.imshow('OCR rotated', rotated)
rotated = imutils.rotate_bound(image, angle=hough_angle*(-1))
cv2.imshow('Hough rotated', rotated)
# rotated_image = cv2.rotate(image, rotateCode=) #image.rotate(ocr_angle, fillcolor="white", expand=True)
rotated_image = np.array(rotated)
save_file(file, rotated_image)
cv2.waitKey(0)