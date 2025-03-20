## Description

Initial instructions:
1. Create a web server with a `/start` endpoint.
   1. It only responds to a POST request.
   2. When it receives the parameter `rtsp_url`, start a new process.
2. The new process reads the video stream from `rtsp_url` using `opencv`.
3. Add a `/stop` endpoint.
   1. Save an image with a size of 900x900 of the top 9 brightest frames from the video in a grid.
   2. Stop the video reading process.
   3. Display the image in the HTML response.

The file `program.py` implements a rudimentary version of those instructions. Your task is to:
- Fix the errors in `program.py` to make it work.
- Capture frames at a specified interval.
- Add logging.
- Handle multiple video streams concurrently. Ensure that each stream can be started and stopped independently.

Notes:
- Your solution will be judged based on readability, correctness and documentation.
- This task should not take more than 1-2 hours.
- Do NOT post your answer on a public URL.

## Submission

- Create a zip file exercise.zip
- After it's unzipped, it should contain the project source code.
- Share the zip on Upwork and list the limitations if any.
- The program MUST run inside Docker. We will run your script using the following command:

```shell
unzip exercise.zip
cd exercise
docker build -t exercise .
docker run -p 8000:8000 -v /path/to/exercise:/app exercise
curl -d "rtsp_url=rtsp://platerec:8S5AZ7YasGc3m4@video.platerecognizer.com:8554/demo" http://localhost:8000/start
curl http://localhost:8000/stop
```