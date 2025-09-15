import time
from vision import Vision
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
import contour
import numpy as np
import cv2


def grab_pen(rot_matrix, tran_matrix):
    vision = Vision()
    vision.get_frame()
    robot = InterbotixManipulatorXS("px100", "arm", "gripper")
    robot_startup()
    robot.gripper.release()
    images, valid = vision.get_aligned_frames()
    if not valid:
        return
    panel, cx, cy, cz = contour.contour_filter(images, vision)
    cv2.imshow('Result', panel)
    if cx == -1 and cy == -1 and cz == -1:
        print("No object detected")
        return
    cam_coord = np.array([cx, cy, cz]).reshape((3,1))
    rob_coord = rot_matrix @ cam_coord + tran_matrix
    print(f"Calculated Robot Coordinates: x: {rob_coord[0][0]}, y: {rob_coord[1][0]}, z: {rob_coord[2][0]}")
    robot.arm.set_ee_pose_components(x=rob_coord[0][0], y=rob_coord[1][0], z=rob_coord[2][0], moving_time=2.0)
    robot.gripper.grasp()
    time.sleep(0.5)
    robot.arm.set_ee_pose_components(x=rob_coord[0][0], y=rob_coord[1][0], z=rob_coord[2][0]+0.1, moving_time=2.0)
    robot.gripper.release()
    robot.arm.go_to_sleep_pose()
    robot_shutdown()


with open("Rotation_mat.txt", "r") as f:
    rot_matrix = np.array([[float(num) for num in line.split()] for line in f.readlines()])
with open("Translation_mat.txt", "r") as f:
    tran_matrix = np.array([[float(num) for num in line.split()] for line in f.readlines()])
grab_pen(rot_matrix, tran_matrix)