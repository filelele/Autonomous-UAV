import threading
import cv2
import numpy as np
import time

class ThreadedCamera():
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame_buffer = None

        self.frame_feeder_thread = threading.Thread(target=self.frame_feeder, daemon=True)
        self.frame_feeder_thread.start()

    def frame_feeder(self):
        consecutive_error_read = 0
        while True:
            ret, frame = self.cam.read()
            if not ret:
                consecutive_error_read += 1
                if consecutive_error_read >= 15:
                    print("Cam error: Failed to get frame\nQuitting\n")
                    exit()
            else:
                consecutive_error_read = 0
                self.frame_buffer = frame

    def read(self):
        while True:
            if self.frame_buffer is not None:
                return self.frame_buffer
            else:
                continue
            
if __name__ == "__main__":
    cam = ThreadedCamera()

    while True:
        frame = cam.read()
        if frame is not None:
            cv2.imshow("Live", frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            print("Quitting: Q pressed\n")
            break

    cv2.destroyAllWindows()
