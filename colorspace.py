import cv2 as cv
import numpy as np


def colorspace_filter(image):
    alpha_slider_max = 180
    title_window = 'Color Space Filter'

    # Convert BGR to HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    if not hasattr(colorspace_filter, "_inited"):
        cv.namedWindow(title_window, cv.WINDOW_NORMAL)     # safe if already exists
        cv.createTrackbar(f'Low x {alpha_slider_max}', title_window, 0, alpha_slider_max, lambda v: None)
        cv.createTrackbar(f'High x {alpha_slider_max}', title_window, 0, alpha_slider_max, lambda v: None)

        colorspace_filter._inited = True

    lower_color = cv.getTrackbarPos(f'Low x {alpha_slider_max}', title_window)
    upper_color = cv.getTrackbarPos(f'High x {alpha_slider_max}', title_window)

    # define range of the color in HSV
    lower_color = np.array([lower_color,10,50], dtype=np.uint8)
    upper_color = np.array([upper_color,255,255], dtype=np.uint8)
    print(f"Low: {lower_color}, High: {upper_color}")
    # Threshold the HSV image to get only the color required
    mask = cv.inRange(hsv, lower_color, upper_color)
    mask_bgr = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(image,image, mask= mask)
    return mask_bgr, mask, res
