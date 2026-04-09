from pysimverse import Drone
import cv2
import numpy as np
import os
import time
import threading
from datetime import datetime
import sys
from io import StringIO

class DroneStreamCapture:
    def __init__(self, drone, output_dir=None, filename=None, display=True, fps=20):
        self.drone = drone
        self.display = display
        self.fps = fps
        self.running = False
        self.writer = None
        self.thread = None
        self.frame_size = None
        self.latest_frame = None
        self.lock = threading.Lock()
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "recordings")
        self.filename = filename or datetime.now().strftime("drone_stream_%Y%m%d_%H%M%S.avi")
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_path = os.path.join(self.output_dir, self.filename)

    def _initialize_writer(self, frame):
        height, width = frame.shape[:2]
        self.frame_size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, self.frame_size)

    def start(self):
        if self.running:
            return
        self.running = True
        self.drone.streamon()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"Drone stream capture started, saving to: {self.output_path}")

    def _run(self):
        while self.running:
            # Suppress stdout to avoid "Failed to decode frame" errors
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                frame, ok = self.drone.get_frame()
            finally:
                sys.stdout = old_stdout

            if ok and frame is not None:
                with self.lock:
                    self.latest_frame = frame.copy()
                if self.writer is None:
                    self._initialize_writer(frame)
                self.writer.write(frame)
                if self.display:
                    cv2.imshow("Drone Stream", frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        self.running = False
                        break
            else:
                time.sleep(0.02)
        self._cleanup()

    def get_latest_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None, False
            return self.latest_frame.copy(), True

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.thread is not None and threading.current_thread() is not self.thread:
            self.thread.join(timeout=2)
        self.drone.streamoff()
        self._cleanup()
        print("Drone stream capture stopped.")

    def _cleanup(self):
        if self.writer is not None:
            self.writer.release()
            self.writer = None
        if self.display:
            cv2.destroyAllWindows()
