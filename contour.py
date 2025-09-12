import cv2 as cv
import colorspace
import vision
import numpy as np

def contour_filter(image):
    thre_bgr, thre_image, _ = colorspace.colorspace_filter(image)
    contours, _ = cv.findContours(thre_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    image_copy = image.copy()
    cv.drawContours(image_copy, contours, -1, (0,255,0), 3)
    panel = np.hstack((image, thre_bgr, image_copy))

    return panel