import pyrealsense2 as rs
import numpy as np
import cv2


class Vision:
    def __init__(self, depth_res=(640,480), color_res=(640,480), fps=30, clip_m=3.0):
        self.depth_res = depth_res
        self.color_res = color_res
        self.fps = fps
        self.clip_m = clip_m

        self.pipeline = None
        self.config = None
        self.profile = None
        self.align = None
        self.clipping_distance = None
        self.aligned_frames = None

        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, *self.depth_res, rs.format.z16, self.fps)
        self.config.enable_stream(rs.stream.color, *self.color_res, rs.format.bgr8, self.fps)



    def get_frame(self):
        self.pipeline = rs.pipeline()
        # Start streaming
        self.profile = self.pipeline.start(self.config)
        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)
        # We will be removing the background of objects more than
        #  clipping_distance_in_meters meters away
        clipping_distance_in_meters = 1 #1 meter
        self.clipping_distance = clipping_distance_in_meters / depth_scale

    
    
    def get_aligned_frames(self):
        self.align  = rs.align(rs.stream.color)
        # Streaming loop
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        self.aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = self.aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = self.aligned_frames.get_color_frame()

        # Validate that both frames are valid
        valid = aligned_depth_frame and color_frame

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > self.clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.3), cv2.COLORMAP_JET)
        #images = np.hstack((bg_removed, depth_colormap))
        return bg_removed, valid