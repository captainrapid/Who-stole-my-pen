import contour
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from vision import Vision
import cv2
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.spatial.transform import Rotation as R

class Calibration:

    def __init__(self):
        self.sample_points_x = [0.1, 0.15, 0.2]
        self.sample_points_y = [-0.03, 0.03]
        self.sample_points_z = [0.15, 0.2]
        self.sample_times = len(self.sample_points_x) * len(self.sample_points_z) * len(self.sample_points_y)
        self.camera_sample_times = 10

    def sampling(self):
        vision = Vision()
        vision.get_frame()
        robot_coordinates = []
        camera_coordinates = []
        robot = InterbotixManipulatorXS("px100", "arm", "gripper")
        robot_startup()
        robot.gripper.grasp()

        for x in self.sample_points_x:
            for y in self.sample_points_y:
                for z in self.sample_points_z:
                    robot.arm.set_ee_pose_components(x=x, y=y, z=z, moving_time=2.0)
                    time.sleep(0.2)
                    p = robot.arm.get_ee_pose()
                    rx, ry, rz = p[0:3, 3]
                    print(f"Robot end-effector position: x: {rx}, y: {ry}, z: {rz}")
                    robot_coordinates.append((rx, ry, rz))
                    images, valid = vision.get_aligned_frames()
                    cx,cy,cz = 0,0,0
                    for _ in range(self.camera_sample_times):
                        _, cx_temp, cy_temp, cz_temp = contour.contour_filter(images, vision)
                        cx += cx_temp
                        cy += cy_temp
                        cz += cz_temp
                        time.sleep(0.02)
                    cx /= self.camera_sample_times
                    cy /= self.camera_sample_times
                    cz /= self.camera_sample_times
                    camera_coordinates.append((cx, cy, cz))
                    if not valid:
                        continue
        robot.arm.go_to_sleep_pose()
        robot_shutdown()
        return robot_coordinates, camera_coordinates
    

    def robo_sampling(self):
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
        robot.arm.go_to_sleep_pose()
        robot_shutdown()
        return robot_coordinates, camera_coordinates
    
    def calculate_transform(self, rob_coord, cam_coord):
        arr_rob = np.array(rob_coord)
        arr_cam = np.array(cam_coord)

        # First calculate rotation
        rob_center = np.mean(arr_rob, axis=0)
        cam_center = np.mean(arr_cam, axis=0)
        rob_centered = arr_rob - rob_center
        cam_centered = arr_cam - cam_center
        rotation_matrix = R.align_vectors(rob_centered, cam_centered)[0].as_matrix()
        rotation_matrix = np.array(rotation_matrix)


        # Then calculate translation
        translation = np.zeros((3,1))
        for i in range(len(rob_coord)):
            translation += (arr_rob[i].reshape((3,1)) - rotation_matrix @ arr_cam[i].reshape((3,1)))
        translation /= len(rob_coord)

        return rotation_matrix, translation


def plot_coords(rob_coord, cam_coord):
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

    x_lims = ax.get_xlim3d()
    y_lims = ax.get_ylim3d()
    z_lims = ax.get_zlim3d()
    x_range = x_lims[1] - x_lims[0]
    y_range = y_lims[1] - y_lims[0]
    z_range = z_lims[1] - z_lims[0]
    plot_radius = 0.5 * max([x_range, y_range, z_range])
    ax.set_xlim3d(np.mean(x_lims) + np.array([-plot_radius, plot_radius]))
    ax.set_ylim3d(np.mean(y_lims) + np.array([-plot_radius, plot_radius]))
    ax.set_zlim3d(np.mean(z_lims) + np.array([-plot_radius, plot_radius]))
    
    ax.legend()

    plt.show()


    
rob_coord, cam_coord = Calibration().sampling()
plot_coords(rob_coord, cam_coord)
rot_mat, tran_mat = Calibration().calculate_transform(rob_coord, cam_coord)
transformed_cam = [rot_mat @ np.array(c).reshape((3,1)) + tran_mat for c in cam_coord]
plot_coords(rob_coord, transformed_cam)
print("Rotation Matrix:\n", rot_mat)
print("Translation Matrix:\n", tran_mat)
np.savetxt("Rotation_mat.txt", rot_mat, fmt='%s')
np.savetxt("Translation_mat.txt", tran_mat, fmt='%s')
