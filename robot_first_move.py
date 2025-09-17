from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
import time

#################Citation 3##################
# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")

robot_startup()
mode = 'h'
# Let the user select the position
while mode != 'q':
    mode=input("[h]ome, [s]leep, [q]uit, [g]rasp, [t]est: ")
    if mode == "h":
        robot.arm.set_trajectory_time(2, 0.3)
        robot.arm.go_to_home_pose()
    elif mode == "s":
        robot.arm.set_trajectory_time(2, 0.3)
        robot.arm.go_to_sleep_pose()
        ###################Citation 3###################
    elif mode == "g":
        robot.gripper.release()
        robot.arm.set_ee_pose_components(x=0.2, y=0.0, z=0.04, pitch=1.4, moving_time=1.0)
        robot.gripper.grasp()
        time.sleep(0.05)
        robot.arm.set_ee_pose_components(x=0.1, y=0.0, z=0.3, pitch=-1.0, moving_time=1.0)
        robot.gripper.release()
    elif mode == "t":
        robot.arm.set_ee_pose_components(x=-0.15, y=0.0, z=0.25, moving_time=2.0)

robot_shutdown()