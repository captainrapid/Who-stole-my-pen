from __future__ import print_function
from __future__ import division
import cv2 as cv
import argparse
    
def trackbar_filter(image):
    alpha_slider_max = 100
    title_window = 'Linear Blend'

    if not hasattr(trackbar_filter, "_inited"):
        cv.namedWindow(title_window, cv.WINDOW_NORMAL)     # safe if already exists
        cv.createTrackbar(f'Alpha x {alpha_slider_max}', title_window, 0, alpha_slider_max, lambda v: None)
        trackbar_filter._inited = True

    src1 = image.copy()
    src2 = cv.cvtColor(src1, cv.COLOR_BGR2GRAY) 
    src2 = cv.cvtColor(src2, cv.COLOR_GRAY2BGR)

    alpha = cv.getTrackbarPos(f'Alpha x {alpha_slider_max}', title_window) / alpha_slider_max
    beta = 1.0 - alpha

    # return the blended current frame
    dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)

    return dst