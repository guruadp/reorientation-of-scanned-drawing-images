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
        angle = angle if (angle>0) else angle + 90
        angles.append(angle)
    
    #cv2.imshow('Lines', image)
    print(angles)
    count = {i: angles.count(i) for i in angles}
    print(count)
    hough_angle = list(count.keys())[list(count.values()).index(max(count.values()))]
    return hough_angle

file = "sample.pdf"
image = pdf_to_image(file)
hough_angle = angle_detection_hough_line(image)
print(f'Angle = {hough_angle}')
cv2.waitKey(0)