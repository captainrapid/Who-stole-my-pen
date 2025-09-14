import contour
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from vision import Vision
import cv2
import time

class Calibration:

    def __init__(self):
        self.sample_points_x = [0.1, 0.15, 0.2]
        self.sample_points_z = [0.1, 0.15, 0.2]
        self.sample_times = 9

    def sampling(self):
        vision = Vision()
        vision.get_frame()
        robot_coordinates = []
        camera_coordinates = []
        robot = InterbotixManipulatorXS("px100", "arm", "gripper")
        robot_startup()
        robot.gripper.grasp()
        for x in self.sample_points_x:
            for z in self.sample_points_z:
                robot.arm.set_ee_pose_components(x=x, y=0.0, z=z, pitch=-0.0, moving_time=3.0)
                time.sleep(1)
                p = robot.arm.get_ee_pose()
                rx, ry, rz = p[0:3, 3]
                print(f"Robot end-effector position: x: {rx}, y: {ry}, z: {rz}")
                robot_coordinates.append((rx, ry, rz))
                images, valid = vision.get_aligned_frames()
                #filtered_image = contour.contour_filter(images)
                panel, cx, cy, cz = contour.contour_filter(images, vision)
                camera_coordinates.append((cx, cy, cz))
                if not valid:
                    continue
                #cv2.imshow('Original', images)
                #cv2.imshow('Filtered', filtered_image)
                cv2.imshow('Result', panel)
        robot.gripper.release()
        robot.arm.go_to_sleep_pose()
        robot_shutdown()
        return robot_coordinates, camera_coordinates
    
rob_coord, cam_coord = Calibration().sampling()
for i in range(len(rob_coord)):
    print("Robot Coordinates: ", rob_coord[i])
    print("Camera Coordinates: ", cam_coord[i])
