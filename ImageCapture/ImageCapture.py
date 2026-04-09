import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pysimverse import Drone
import time
from Controller.KeyboardController import KeyboardController
from Stream.stream import DroneStreamCapture

class ImageCapture:

    def __init__(self):
        self.drone = Drone()
        self.drone.connect()
        self.drone.set_speed(200)
        self.drone.set_rotation_speed(100)
        images_dir = os.path.join(os.path.dirname(__file__), "images")
        self.stream_capture = DroneStreamCapture(self.drone)
        self.controller = KeyboardController(self.drone, images_dir=images_dir, stream_capture=self.stream_capture)

    def start(self):
        print("Controlling drone with keyboard. Press keys to move:")
        print("T: takeoff, L: land")
        print("W: forward, S: backward, A: left, D: right")
        print("Q: rotate left, E: rotate right")
        print("Up arrow: up, Down arrow: down")
        print("Z: capture image")
        print("Press Ctrl+C to stop")

        self.stream_capture.start()

        try:
            self.controller.start()
        except KeyboardInterrupt:
            pass
        finally:
            self.controller.stop()
            self.stream_capture.stop()
            self.drone.land()

if __name__ == "__main__":
    imgc = ImageCapture()
    imgc.start()
