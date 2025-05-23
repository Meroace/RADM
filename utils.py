import cv2
import numpy as np
from PIL import Image

def image_to_array(image: Image.Image) -> np.ndarray:
    return np.array(image)

def start_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Unable to access the webcam.")
    return cap

def release_webcam(cap):
    if cap and cap.isOpened():
        cap.release()
