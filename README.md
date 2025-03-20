None selected 

Skip to content
Using Gmail with screen readers
Conversations
Coding Exercise
Inbox
Interview Details
Job Search

Marc Belmont
Wed, Mar 19, 11:04 AM (1 day ago)
Hi, Ky enjoyed chatting with you on Monday, and we would like to continue the interview process. The next step is for you to work on a coding exercise. When wou
6

Leon Jaggon <leonojaggon@gmail.com>
Attachments
2:53 PM (3 hours ago)
to Marc

This documentation should've been added as well, it was edited outside of my IDE and got placed in a different folder.

 One attachment
  •  Scanned by Gmail

Marc Belmont
3:12 PM (2 hours ago)
to me

Thanks, I'll check it out! There's no need to use Upwork.

Awesome, thank you so much!Thanks, I'll check it out!Awesome, thanks for letting me know.
# Video Processing API Documentation

## Endpoints

### 1. Start video stream processing  (`/start`)

**Method:** `POST`

This endpoint starts a new video stream using an RTSP URL and captures frames. It processes the video stream and captures frames at regular intervals specified.

#### Parameters:

- **Form data:**
  - `rtsp_url` (string): The RTSP stream URL to capture video from.
- **Query parameters:**
  - `capture_interval` (integer, optional): The interval (in seconds) between each frame capture.

#### Responses:

​	**200 OK**: Stream started successfully.

- JSON response:

  ```
  {
    "status": "Video stream started",
    "stream_id": "unique_stream_id"
  }
  ```

​	**400 Bad Request**: Missing `rtsp_url`.

- Response:

  ```
  Missing RTSP URL
  ```

### 2. List all currently processing streams (`/list`)

**Method:** `GET`

This endpoint lists all active video streams along with their current state.

#### Responses:

​	**200 OK**: Successfully returns the list of active streams.

- JSON response:

  ```
  {
    "active_streams": {
      "stream_id_1": {
        "frames_captured": 100,
        "url": "rtsp://example.com/stream1",
        "running_time": 120.5
      },
      "stream_id_2": {
        "frames_captured": 50,
        "url": "rtsp://example.com/stream2",
        "running_time": 65.3
      }
    }
  }
  ```

### 3. Get Stream Status (`/status/<stream_id>`)

**Method:** `POST`

This endpoint provides the status of a specific stream.

#### Parameters:

- URL parameters:
  - `stream_id` (string): The unique identifier for the stream.

#### Responses:

​	**200 OK**: Stream status.

- Response:

  ```
  "Stream status: Active"
  ```

​	**404 Not Found**: Stream with the provided ID doesn't exist.

- Response:

  ```
  Stream not found with id <stream_id>
  ```

### 4. Stop Stream (`/stop/<stream_id>`)

**Method:** `POST`

This endpoint stops a specific stream and processes its frames to generate a grid of the brightest frames captured during the stream.

#### Parameters:

- URL parameters:
  - `stream_id` (string): The unique identifier for the stream.

#### Responses:

- **200 OK**: Successfully stops the stream and returns the brightest frame grid as a JPEG image.

  - The image will be returned as the response body.

- **404 Not Found**: Stream with the provided ID doesn't exist.

  - Response:

    ```
    Stream ID <stream_id> not found
    ```

- **400 Bad Request**: No frames captured by the stream.

  - Response:

    ```
    No frames captured
    ```

- **500 Internal Server Error**: Failure in image processing.

  - Response:

    ```
    Failed to create image
    ```

### 5. Stop All Streams (`/stop`)

**Method:** `POST`

This endpoint stops all active video streams. It will terminate any running processes for all streams and return a status for each stream.

#### Responses:

- 200 OK

  : Successfully stops all streams.

  - JSON response:

    ```
    {
      "results": {
        "stream_id_1": "Stopped",
        "stream_id_2": "Stopped"
      }
    }
    ```
Video Processing API Documentation.md
Displaying Video Processing API Documentation.md.
