import pyrealsense2 as rs
import cv2
from vision import Vision
import colorspace
import numpy as np
import contour

def main():
    vision = Vision()
    vision.get_frame()

    while True:
        images, valid = vision.get_aligned_frames()
        #filtered_image = contour.contour_filter(images)
        panel, _, _, _ = contour.contour_filter(images, vision)
        if not valid:
            continue
        #cv2.imshow('Original', images)
        #cv2.imshow('Filtered', filtered_image)
        cv2.imshow('Result', panel)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()