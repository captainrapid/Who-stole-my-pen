import vision
import pyrealsense2 as rs

def position(vision: vision.Vision, cx, cy):
    depth = vision.aligned_frames.get_depth_frame().get_distance(cx, cy)
    profile = vision.profile.get_stream(rs.stream.color)
    intr = profile.as_video_stream_profile().get_intrinsics()
    x, y, z = rs.rs2_deproject_pixel_to_point(intr, [cx, cy], depth)
    print(f"The position is x: {x}, y: {y}, z: {z}")
    return x, y, z