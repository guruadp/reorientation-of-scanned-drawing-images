import cv2
from pdf2image import convert_from_path
import numpy as np
import math
import pytesseract
import re

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
    # image = rescaleFrame(image, 0.5)
    # cv2.imshow('Image', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)   
    cv2.imwrite(r'output/gray.jpg', gray)
    # cv2.imshow('Gray Image', gray) 
    _,binary = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    cv2.imwrite(r'output/binary.jpg', binary)
    # cv2.imshow('Threshold', binary)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel1)
    # cv2.imshow('Opening', opening)
    canny = cv2.Canny(binary, 50, 150, apertureSize=3)    
    cv2.imwrite(r'output/canny.jpg', canny)
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
        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        angle = math.atan2(y2 - y1, x2 - x1) 
        angle = round(math.degrees(angle), 1)
        # angle = angle if (angle>0) else angle + 90
        angles.append(angle)
    cv2.imwrite(r'output/hough.jpg', image)
    #cv2.imshow('Lines', image)
    count = {i: angles.count(i) for i in angles}
    hough_angle = list(count.keys())[list(count.values()).index(max(count.values()))]
    return hough_angle

def angle_detection_ocr(filepath):
    print(str(filepath))
    image = cv2.imread('sample.jpg')
    cv2.imshow('IMage', image)
    results = pytesseract.image_to_osd(image)
    return 0

def rotate_image(image, angle):
    image = cv2.imread(image)
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=(255,255,255))
    return rotated

def save_file(filename, img_rotated):
    filename = str(filename.split(".")[0]) + "_rotated.jpg"
    cv2.imwrite(filename, img_rotated)
    return filename

filename = "sample.pdf"
image = pdf_to_image(filename)
hough_angle = angle_detection_hough_line(image)
print(f'Hough angle = {hough_angle}')

rotated_image = rotate_image(image, angle=hough_angle)
rotated_image_filename = save_file(filename, rotated_image)

results = pytesseract.image_to_osd(rotated_image_filename)
ocr_angle = re.search('(?<=Orientation in degrees: )\d+', results).group(0)
print(f'OCR angle = {ocr_angle}')

rotated_image = rotate_image(rotated_image_filename, angle=int(ocr_angle))
rotated_image_filename = save_file(filename, rotated_image)

cv2.waitKey(0)