FROM nvidia/cuda:12.2.0-runtime-ubuntu20.04

# Avoid interactive prompts during build (tzdata fix)
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tzdata python3.8 python3-pip git ffmpeg && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    ln -s /usr/bin/python3.8 /usr/bin/python && \
    pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY ./app ./app

# Default run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
