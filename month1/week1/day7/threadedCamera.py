import threading
import cv2
import multiprocessing

class ThreadedCamera():
    def __init__(self):
        self.t = threading.Thread(target=self.readToBuffer)
        self.t.start()
        self.buffer_frame = None
        self.cap = None

    def readToBuffer(self):
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        while True:
            ret, self.buffer_frame = self.cap.read()
            if not ret:
                print("Camera error: Cannot read from camera\n")
                self.cap.release()
                exit()

    def read(self):
        while True:
            if self.buffer_frame is not None:
                return self.buffer_frame
            else:
                continue


    
