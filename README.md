# ModelScope Text-to-Video Generation API

This project wraps the ModelScope `text-to-video-synthesis` model with a FastAPI server, ready to deploy on Render with GPU.

## 🚀 Usage

1. Clone the repo and run:

```bash
docker build -t video-api .
docker run --gpus all -p 8000:8000 video-api
