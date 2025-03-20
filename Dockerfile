FROM python:3.10-slim

WORKDIR /app

COPY . /app

# environment variables to avoid writing .pyc files and ensure unbuffered output
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# needed build tools to compile openvc from source
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install opencv with pip seems to hang, this alternative is way faster
RUN apt-get update
RUN apt-get install -y python3-opencv

RUN python3 -m venv /venv

RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt

EXPOSE 5000

# run app in venv, unnecessary but I used one locally so why not
CMD ["/venv/bin/python", "src/program.py"]
