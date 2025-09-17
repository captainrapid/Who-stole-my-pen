# Who stole my pen?

## Overview
This project provides a complete pipeline for calibrating a robot arm with a RealSense camera, detecting a pen using computer vision, and commanding the robot to pick up the pen. The robot arm is the Interbotix PX100 robotic arm, and the camera is a Realsense camera that returns both RGB stream and depth stream.

## File Structure
- `main.py`: Runs the real-time vision and detection loop.
- `calibration.py`: Handles calibration between the camera and robot, including sampling and transformation calculation.
- `vision.py`: Manages RealSense camera streaming, frame alignment, and background removal.
- `colorspace.py`: Provides color filtering using HSV and OpenCV trackbars.
- `contour.py`: Detects contours and computes centroids for object localization.
- `position.py`: Converts 2D image coordinates to 3D camera coordinates using depth data.
- `grab_pen.py`: Uses the calibration results to command the robot to pick up the detected pen.
- `thread.py`: Example of running calibration and main loop in separate threads.
- `Rotation_mat.txt`, `Translation_mat.txt`: Saved transformation matrices from calibration.
- `citation.txt`: Citations and references for used algorithms or code.

## Requirements
- Python 3.8+
- [Interbotix PX100 Arm](https://www.trossenrobotics.com/interbotix-px100-robot-arm.aspx)
- Intel RealSense Depth Camera (e.g., D435)
- Ubuntu Linux (recommended)

### Python Packages
- `pyrealsense2`
- `opencv-python`
- `numpy`

## Notes
- Adjust color filtering parameters in `colorspace.py` using the OpenCV trackbars for your specific pen color.In this program, hue range between 51 and 88 to track GREEN color under warm lighting condition.
- Ensure the robot and camera are securely mounted and have overlapping workspaces.
- The calibration process requires the robot to move to several positions; ensure the area is clear.
- Use `main.py` to check the working space for camera before calibration.

## Citations
See `citation.txt` for references to algorithms and code snippets used in this project.

- `matplotlib`
- `scipy`
- `interbotix_xs_modules` 
