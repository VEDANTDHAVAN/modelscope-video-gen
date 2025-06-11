FROM nvidia/cuda:12.2.0-cudnn8-runtime-ubuntu20.04

# Set timezone to avoid tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt-get update && \
    apt-get install -y python3.8 python3-pip git ffmpeg tzdata && \
    ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    ln -s /usr/bin/python3.8 /usr/bin/python && \
    python -m pip install --upgrade pip

# Set work directory
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
