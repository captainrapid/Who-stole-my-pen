import contour
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from vision import Vision
import cv2
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Calibration:

    def __init__(self):
        self.sample_points_x = [0.1, 0.15, 0.2]
        self.sample_points_z = [0.15, 0.2]
        self.sample_times = len(self.sample_points_x) * len(self.sample_points_z)

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
                robot.arm.set_ee_pose_components(x=x, y=0.0, z=z, moving_time=2.0)
                time.sleep(3)
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
        #robot.gripper.release()
        robot.arm.go_to_sleep_pose()
        robot_shutdown()
        return robot_coordinates, camera_coordinates
    
rob_coord, cam_coord = Calibration().sampling()
for i in range(len(rob_coord)):
    print("Robot Coordinates: ", rob_coord[i])
    #print("Camera Coordinates: ", cam_coord[i])

# Convert lists of tuples into separate coordinate lists
rx, ry, rz = zip(*rob_coord)
cx, cy, cz = zip(*cam_coord)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter robot coords (blue) and camera coords (red)
ax.scatter(rx, ry, rz, c='b', marker='o', label='Robot Coords')
ax.scatter(cx, cy, cz, c='r', marker='^', label='Camera Coords')

# Label axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.show()
