import cv2 as cv
import colorspace
import vision
import numpy as np

def contour_filter(image):
    thre_bgr, thre_image, _ = colorspace.colorspace_filter(image)
    contours, _ = cv.findContours(thre_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    max_length = 0
    max_contour = None
    for contour in contours:
        length = cv.arcLength(contour, True)
        if length > max_length:
            max_length = length
            max_contour = contour
    contour = max_contour
    thre_bgr_copy = thre_bgr.copy()
    cv.drawContours(thre_bgr_copy, contour, -1, (0,255,0), 3)
    panel = np.hstack((image, thre_bgr, thre_bgr_copy))

    return panel