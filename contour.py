import cv2 as cv
import colorspace
import vision
import numpy as np

def contour_filter(image):
    _, thre_image, _ = colorspace.colorspace_filter(image)
    contours, _ = cv.findContours(thre_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0,255,0), 3)

    return #contours