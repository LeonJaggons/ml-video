import io
import multiprocessing
import os
import time
import uuid

import cv2
import numpy as np
from flask import Flask, request, send_file, jsonify

from util import capture_frames, get_frames_brightnesses, get_n_maxes, init_logger

logger = init_logger()

streams = {}
app = Flask(__name__)

# For some reason, explicitly setting the env variable was needed for the test stream
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


@app.route("/start", methods=["POST"])
def start():
    global streams
    logger.info("Starting new stream processing")

    rtsp_url = request.form.get("rtsp_url")
    if rtsp_url is None:
        logger.warning("Start request missing RTSP URL")
        return "Missing RTSP URL", 400

    # Generate a unique ID for this stream and create list from Manager to track frames
    stream_id = str(uuid.uuid4())
    logger.info(f"Generated stream ID: {stream_id} for URL: {rtsp_url}")

    manager = multiprocessing.Manager()
    frames = manager.list()

    # Spawn new worker process for this stream
    interval = request.args.get("capture_interval")
    if interval is not None:
        interval = int(interval)

    process = multiprocessing.Process(
        target=capture_frames,
        args=(rtsp_url, frames, stream_id, interval)
    )
    process.start()
    logger.info(f"Process started for stream {stream_id} with PID: {process.pid}")

    # Store stream information in streams
    streams[stream_id] = {
        "process": process,
        "frames": frames,
        "url": rtsp_url,
        "start_time": time.time()
    }

    return jsonify({"status": "Video stream started", "stream_id": stream_id}), 200


@app.route("/list", methods=["GET"])
def list_all_streams():
    global streams
    logger.info("Listing active streams")
    active_streams = {}

    for stream_id, data in streams.items():
        if data["process"].is_alive():
            active_streams[stream_id] = {
                "frames_captured": len(data["frames"]),
                "url": data["url"],
                "running_time": time.time() - data["start_time"]
            }

    logger.info(f"Found {len(active_streams)} active streams")
    return jsonify({"active_streams": active_streams}), 200


@app.route("/status/<stream_id>", methods=["POST"])
def get_stream_status(stream_id):
    global streams
    if stream_id not in streams:
        return f"Stream not found with id {stream_id}", 404
    stream_status = streams[stream_id]["status"]
    return stream_status, 200


@app.route("/stop/<stream_id>", methods=["POST"])
def stop_stream(stream_id):
    global streams
    logger.info(f"Stopping video stream {stream_id}")

    if stream_id not in streams:
        logger.warning(f"Stream ID {stream_id} not found")
        return f"Stream ID {stream_id} not found", 404

    stream_data = streams[stream_id]
    process = stream_data["process"]
    frames = stream_data["frames"]

    if process is not None and process.is_alive():
        logger.info(f"Terminating process for stream {stream_id}")
        process.terminate()
        process.join()

    frame_count = len(frames)
    logger.info(f"Frames captured for stream {stream_id}: {frame_count}")

    # Clean up streams in the event of failed processing i.e errored out process
    if frame_count == 0:
        del streams[stream_id]
        logger.warning(f"No frames captured for stream {stream_id}")
        return "No frames captured", 400

    local_frames = list(frames)

    # Determine [0, 9] brightest frames based on frames available
    brightnesses = get_frames_brightnesses(local_frames)
    top_indices, top_brightnesses = get_n_maxes(brightnesses, 9)
    top_frames = [local_frames[i] for i in top_indices]

    # Create 3x3 image grid
    num_frames = len(top_frames)
    grid_size = min(3, max(1, int(np.ceil(np.sqrt(num_frames)))))
    logger.info(f"Creating {grid_size}x{grid_size} grid with {num_frames} frames")

    grid_image = np.zeros((grid_size * 300, grid_size * 300, 3), dtype=np.uint8)
    for i, frame in enumerate(top_frames):
        if i >= grid_size * grid_size:
            break
        resized_frame = cv2.resize(frame, (300, 300))
        row = (i // grid_size) * 300
        col = (i % grid_size) * 300
        grid_image[row: row + 300, col: col + 300] = resized_frame

    # Convert to PIL Image and save to memory buffer instead of file
    logger.info("Encoding final grid image " + stream_id)
    success, buffer = cv2.imencode(".jpg", grid_image)

    # Cleanup stream data after processing
    logger.info(f"Cleaning up stream {stream_id}")
    del streams[stream_id]

    if not success:
        logger.error("Failed to create grid image ", stream_id)
        return "Failed to create image", 500

    logger.info("Returning grid image")
    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)

    return send_file(io_buf, mimetype="image/jpeg")


@app.route("/stop", methods=["POST"])
def stop_all_streams():
    global streams
    logger.info("Stopping all active streams")
    results = {}

    # Check if process for each stream is still alive and if so, terminates it
    for stream_id in list(streams.keys()):
        try:
            process = streams[stream_id]["process"]
            if process is not None and process.is_alive():
                logger.info(f"Terminating process for stream {stream_id}")
                process.terminate()
                process.join()
            results[stream_id] = "Stopped"
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error stopping stream {stream_id}: {error_msg}")
            results[stream_id] = f"Error: {error_msg}"

    logger.info(f"Cleared {len(streams)} streams")
    streams.clear()

    return jsonify({"results": results}), 200


def init():
    global streams
    streams = {}


if __name__ == "__main__":
    init()
    multiprocessing.set_start_method('spawn', force=True)
    logger.info("Starting server")
    app.run(host="0.0.0.0", port=8000, debug=False)
