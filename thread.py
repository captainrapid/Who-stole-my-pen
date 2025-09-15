import threading
from calibration import Calibration#, plot_coords
from main import main

def stream_thread():
    calibration = Calibration()
    rob_coord, cam_coord = calibration.robo_sampling()
    #plot_coords(rob_coord, cam_coord)

threading.Thread(target=stream_thread).start()

main()

