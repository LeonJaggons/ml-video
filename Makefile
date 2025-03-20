IMAGE_NAME = video-stream-processor

build:
	docker build -t $(IMAGE_NAME) .

run:

clean:
	docker rm -f $(shell docker ps -a -q) || true
	docker rmi -f $(IMAGE_NAME) || true

rebuild: clean build run