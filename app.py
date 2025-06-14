from modal import App, fastapi_endpoint, Image

from pydantic import BaseModel
# Step 1: Define the image with PyTorch (CPU version)
image = (
    Image.debian_slim(python_version="3.10")
    .apt_install("libgl1", "libglib2.0-0", "ffmpeg")  # ✅ Fix for libGL.so.1 error
    .run_commands(
        "pip install torch torchvision",
        "pip install transformers",
        "pip install modelscope datasets==2.18.0 accelerate addict opencv-python pillow simplejson sortedcontainers einops fastapi[standard] open_clip_torch"
    )
)

class VideoPrompt(BaseModel):
    prompt: str

# Step 2: Define the Modal App
app = App("modelscope-text2video")

# Step 3: Define the function
@app.function( image=image, gpu="A10G", timeout=900)
@fastapi_endpoint(method="POST")
def generate_video(request: VideoPrompt):
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks

    text_to_video = pipeline(Tasks.text_to_video_synthesis, model='iic/text-to-video-synthesis')
    result = text_to_video({'text': request.prompt})
    return {"video_path": result['output_path']}
