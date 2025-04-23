import argparse
import os
from threadedCamera import ThreadedCamera
import Filter
import multiprocessing
import cv2

def getDirImage_process(dir, queue_out):
    img_list = os.listdir(dir)
    num_img = len(img_list)
    for img_path in img_list:
        img = cv2.imread(os.path.join(dir,img_path))
        queue_out.put(img)

def getCamFrame_process(queue_out):
    cam = ThreadedCamera()
    while True:
        frame = cam.read()
        queue_out.put(frame)

def filtering_process(queue_in, queue_out_dir, queue_out_live_display, filters):
    """
    Accept a list of filters in Function Object form
    Get frame from queue_in, apply function object to frame, then push to queue_out
    """
    while True:
        frame = queue_in.get()
        for filter_func in filters:
            frame = filter_func(frame)
        queue_out_dir.put(frame)
        if queue_out_live_display is not None:
            queue_out_live_display.put(frame)

def displaying_process(queue_in):
    while True:
        frame = queue_in.get()
        cv2.imshow("Live",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass


if __name__ == "__main__":
    # Get arguments ready
    pparse = argparse.ArgumentParser(description="preprocessing a folder of images\n")
    pparse.add_argument("-i","--input_dir", 
                        type=str, 
                        nargs="?",
                        default="./dontcare/", 
                        help="Original images directory\n")
    pparse.add_argument("-o", "--output_dir", type=str, default="./output", help="Output directory\n")
    pparse.add_argument("-l","--log", action="store_true", help="Write log file\n")
    pparse.add_argument("-f","--filter", 
                        nargs = "+", 
                        choices=["gray", "canny", "blur"],
                        default=["gray"], 
                        help="Choose filter to apply\n")
    pparse.add_argument("-c","--cam_input", action="store_true", help="Switch to camera input\n")
    pparse.add_argument("-d", "--live_display", action="store_true", help="Live display")
    args = pparse.parse_args()

    # Check valid input directory (if args.cam_input is False)
    if not args.cam_input:
        try:
            num_img = len(os.listdir(args.input_dir))
            print(f"Input directory: {args.input_dir} found: {num_img} images.\n")
            if num_img < 1:
                print("Empty directory: Quitting\n")
                exit()
        except FileNotFoundError:
            
            print("Input directory does not exist.\n")
            exit()

    # Check valid output directory
    try:
        os.listdir(args.output_dir)
    except FileNotFoundError:
        print("Output directory not found, one is created.\n")
        os.mkdir(args.output_dir)
    
    # Text argument to corresponding filter function
    filters = []
    for name in args.filter:
        if name == "gray":
            filters.append(Filter.Gray)
        elif name == "canny":
            filters.append(Filter.Canny)
        elif name == "blur":
            filters.append(Filter.Blur)


    # Queue ready
    queue_in2process = multiprocessing.Queue(maxsize=10)
    queue_process2out_dir = multiprocessing.Queue(maxsize=10)
    if args.live_display is True:
        queue_process2out_display = multiprocessing.Queue(maxsize=10)

    # Input process ready:
    if args.cam_input:
        feeder = multiprocessing.Process(target=getCamFrame_process, args=(queue_in2process,))
    else:
        feeder = multiprocessing.Process(target=getDirImage_process, args=(args.input_dir,queue_in2process))

    # Filtering process ready:
    if args.live_display:
        filtering = multiprocessing.Process(target=filtering_process, 
                                            args=(queue_in2process, queue_process2out_dir, queue_process2out_display, filters))
    else:
        filtering = multiprocessing.Process(target=filtering_process, 
                                            args=(queue_in2process, queue_process2out_dir, None, filters))

    # Live display process ready
    if args.live_display:
        displaying = multiprocessing.Process(target=displaying_process,
                                             args=(queue_process2out_display,))
        displaying.start()

    # Initiate processes and run
    feeder.start()
    filtering.start()


    # Output process is also main/parent process
    indexing = 0
    while True:
        try:
            to_write = queue_process2out_dir.get()
            if not indexing%1:
                output_path = os.path.join(args.output_dir, 
                                        f"frame_{indexing}_{int(multiprocessing.current_process().pid)}.jpg")
                cv2.imwrite(output_path, to_write)
            indexing+=1
        except KeyboardInterrupt:
            feeder.terminate()
            filtering.terminate()
            if args.live_display:
                displaying.terminate()
            cv2.destroyAllWindows()
            exit()


