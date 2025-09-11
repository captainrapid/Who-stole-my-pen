import pyrealsense2 as rs
import cv2
from vision import Vision

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

    try:
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
    except Exception as e:
        print("Error:", e)
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()