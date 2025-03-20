import logging
import os
import time
from datetime import datetime

import cv2
import numpy as np

LOG_ROOT = "src/logs/"
DATA_ROOT = "src/data/"


def init_logger():
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_name = f"log_{current_time}.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_ROOT + log_file_name),
        ]
    )
    logger = logging.getLogger("stream_processing_api")
    return logger


def capture_frames(rtsp_url, shared_frames, stream_id, interval):
    if interval is None:
        interval = 1

    process_logger = logging.getLogger(f"video_processor.stream.{stream_id}")
    process_logger.info(f"Starting frame capture for stream {stream_id}")

    # Attempt to find local stream file, if not use url as provided
    stream_url = f"src/data/{rtsp_url}"
    if not os.path.exists(stream_url):
        stream_url = rtsp_url

    cap = cv2.VideoCapture(stream_url)
    last_cap_time = 0

    if not cap.isOpened():
        process_logger.error(f"Failed to open RTSP URL: {rtsp_url}")
        return

    while cap.isOpened():
        curr_time = time.time()
        interval_elapsed = (curr_time - last_cap_time) >= interval
        if interval_elapsed:
            last_cap_time = curr_time
            ret, frame = cap.read()

            if not ret:
                process_logger.warning(f"Failed to read frame from stream {stream_id}")
                break
            shared_frames.append(frame)
            if len(shared_frames) % 10 == 0:
                process_logger.info(f"Stream {stream_id}: Processing {len(shared_frames)} frames")

    process_logger.info(f"Closing capture for stream {stream_id}")
    cap.release()


def calculate_frame_brightness(frame):
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(grayscale_frame)
    return brightness


def get_frames_brightnesses(all_frames):
    brightnesses = [calculate_frame_brightness(frame) for frame in all_frames]
    return brightnesses


def get_n_maxes(arr, n):
    n = min(n, len(arr))
    sorted_indices = np.argsort(arr)[::-1][:n]
    return sorted_indices, [arr[i] for i in sorted_indices]
