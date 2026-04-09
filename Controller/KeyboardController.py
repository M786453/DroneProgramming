from pynput import keyboard
from pynput.keyboard import Key
from pysimverse import Drone
import time
import cv2
import os
from datetime import datetime
import sys
from io import StringIO

class KeyboardController:
    def __init__(self, drone, images_dir=None, stream_capture=None):
        self.drone = drone
        self.keys_pressed = set()
        self.running = False
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.images_dir = images_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "ImageCapture", "images")
        os.makedirs(self.images_dir, exist_ok=True)
        self.stream_capture = stream_capture

    def capture_image(self):
        frame = None
        ok = False

        if self.stream_capture is not None:
            frame, ok = self.stream_capture.get_latest_frame()

        if not ok or frame is None:
            # Suppress stdout to avoid "Failed to decode frame" errors
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                frame, ok = self.drone.get_frame()
            finally:
                sys.stdout = old_stdout

        if not ok or frame is None:
            print("No frame available to capture.")
            return

        filename = datetime.now().strftime("capture_%Y%m%d_%H%M%S_%f.png")
        path = os.path.join(self.images_dir, filename)
        cv2.imwrite(path, frame)
        print(f"Captured image: {path}")

    def on_press(self, key):
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
            if k == 't':
                self.drone.take_off(50, 200)
            elif k == 'l':
                self.drone.land()
            elif k == 'z':
                self.capture_image()
            else:
                self.keys_pressed.add(k)
        else:
            self.keys_pressed.add(key)

    def on_release(self, key):
        if hasattr(key, 'char') and key.char:
            k = key.char.lower()
            self.keys_pressed.discard(k)
        else:
            self.keys_pressed.discard(key)

    def handle_movement(self):
        # Movement controls
        if 'w' in self.keys_pressed:
            self.drone.move_forward(10)
        if 's' in self.keys_pressed:
            self.drone.move_backward(10)
        if 'a' in self.keys_pressed:
            self.drone.move_left(10)
        if 'd' in self.keys_pressed:
            self.drone.move_right(10)
        if 'q' in self.keys_pressed:
            self.drone.rotate(-10)
        if 'e' in self.keys_pressed:
            self.drone.rotate(10)
        if Key.up in self.keys_pressed:  # up
            self.drone.move_up(10)
        if Key.down in self.keys_pressed:  # down
            self.drone.move_down(10)

    def start(self):
        self.running = True
        self.listener.start()
        while self.running:
            self.handle_movement()
            time.sleep(0.05)  # faster loop for smoother control

    def stop(self):
        self.running = False
        self.listener.stop()
