import cv2
import numpy as np

def compute_feature_vector(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image from: {image_path}")
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist
