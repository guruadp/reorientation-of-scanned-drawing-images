import cv2
import numpy as np

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

img = cv2.imread('sample.jpg')

img = rescaleFrame(img, 0.5)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
ret,binary = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
cv2.namedWindow('BGR')
# define a null callback function for Trackbar
def null(x):
    pass

# create three trackbars for B, G and R 
# arguments: trackbar_name, window_name, default_value, max_value, callback_fn
cv2.createTrackbar("Threshold", "BGR", 0, 255, null)
while True:
    # read the Trackbar positions
    b = cv2.getTrackbarPos('Threshold','BGR')
    # change the image colour to Trackbar positions
    ret,binary = cv2.threshold(gray,b,255,cv2.THRESH_BINARY)
    # display trackbars and image
    cv2.imshow('BGR', binary)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows() 