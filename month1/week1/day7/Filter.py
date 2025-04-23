import cv2

def Canny(frame):
    if frame.ndim == 2:  # Grayscale image
        return (255 - cv2.Canny(frame, 5, 30))
    elif frame.ndim == 3 and frame.shape[2] == 3:  # Color image
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return (255 - cv2.Canny(gray_frame, 5, 30))
    else:
        raise ValueError("Unsupported frame format")

def Blur(frame):
    return cv2.GaussianBlur(frame, (5,5), 0)

def Gray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
