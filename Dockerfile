FROM nvidia/cuda:12.2.0-runtime-ubuntu20.04
# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3.8 python3-pip git ffmpeg && \
    ln -s /usr/bin/python3.8 /usr/bin/python && \
    pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app

# Set default run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
