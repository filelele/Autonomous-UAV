"""
Create a script filter_pipeline.py that:

Uses multiprocessing.Process to split work into three parallel processes:

Reader Process: Pulls frames from ThreadedCamera and pushes them to a multiprocessing.Queue.

Filter Process: Receives frames from the queue, applies a filter (e.g., grayscale or Canny edge), and pushes the result to another queue.

Writer Process: Saves the processed frame to disk or displays it with OpenCV.

🧩 Use multiprocessing.Queue for communication and multiprocessing.Event to safely exit all processes.
"""

from camera_thread import ThreadedCamera
import multiprocessing
import cv2
import time
import numpy as np

def filter(queue_in, queue_out):
    """
    tinkering this func to apply different image filterings for the pipeline
    """
    while True:
        frame = queue_in.get()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        edges = cv2.Canny(frame, 20, 100)
        queue_out.put(edges)

def fpsInfor100Frame(list):
    time = np.uint64(0)
    for end, start in list:
        time += np.uint64(end - start)
    time = (time/100)*(10**-9)
    print(f"FPS: {1/time}")

def read_frame(queue_out):
    cam = ThreadedCamera()
    while True:
        frame = cam.read()
        if frame is not None:
            queue_out.put(frame)

if __name__ == "__main__":
    shared_queue_cam2process = multiprocessing.Queue(maxsize=5)
    shared_queue_process2disp = multiprocessing.Queue(maxsize=5)

    read_frame_process = multiprocessing.Process(target=read_frame, args=(shared_queue_cam2process,), daemon=True)
    filter_process = multiprocessing.Process(target=filter, args=(shared_queue_cam2process,shared_queue_process2disp), daemon=True)
    read_frame_process.start()
    filter_process.start()

    count = 0
    local_fps = []
    while True:
        try:
            start = time.perf_counter_ns()
            frame = shared_queue_process2disp.get() # Will slowdown if nothing is pushed from filter_process
            cv2.imshow("Live", frame)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                read_frame_process.terminate()
                filter_process.terminate()
                cv2.destroyAllWindows()
                fpsInfor100Frame(local_fps)
                break
            end = time.perf_counter_ns()
            if count<100:
                local_fps.append((end,start))
                count+=1
            
        except KeyboardInterrupt:
            read_frame_process.terminate()
            filter_process.terminate()
            cv2.destroyAllWindows()
            fpsInfor100Frame(local_fps)
            break
