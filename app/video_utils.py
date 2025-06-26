import cv2
import os
from uuid import uuid4

def extract_frames(video_path: str, output_dir: str, interval_sec: int = 1) -> list:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(fps * interval_sec)
    frame_paths = []

    count = 0
    saved = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval_frames == 0:
            filename = f"{uuid4().hex}.jpg"
            frame_path = os.path.join(output_dir, filename)
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)
            saved += 1
        count += 1
    cap.release()
    return frame_paths
