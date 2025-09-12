from __future__ import print_function
import cv2 as cv
import numpy as np


max_value = 255
max_value_H = 360//2
low_H = 0
high_H = max_value_H
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
high_H_name = 'High H'

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)


def threshold_filter(image):
    cv.namedWindow(window_capture_name)
    cv.namedWindow(window_detection_name)
    cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
    cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)  
    
    frame_HSV = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, 10, 10), (high_H, 255, 255))
    frame_threshold_bgr = cv.cvtColor(frame_threshold, cv.COLOR_GRAY2BGR)
    print('min is', type(min), 'max is', type(max))
    print('cv is', type(cv), 'setTrackbarPos is', type(cv.setTrackbarPos))
    return np.hstack((frame_HSV, frame_threshold_bgr))

