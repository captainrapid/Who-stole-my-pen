import pyrealsense2 as rs
import cv2
from vision import Vision
import trackbar
import colorspace
import numpy as np
import threshold

def main():
    vision = Vision()
    vision.get_frame()
    '''with vision.pipeline:
        while True:
            images, valid = vision.get_aligned_frames()
            if not valid:
                continue
            cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
            cv2.imshow('Align Example', images)
            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

    cv2.destroyAllWindows()'''

    while True:
        images, valid = vision.get_aligned_frames()
        filtered_image = colorspace.colorspace_filter(images)
        if not valid:
            continue
        #cv2.imshow('Original', images)
        #cv2.imshow('Filtered', filtered_image)
        result_image = np.hstack((images, filtered_image))
        cv2.imshow('Result', result_image)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()