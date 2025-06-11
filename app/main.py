from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import traceback

app = FastAPI()

# Optional: Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# Initialize pipeline later
text_to_video = None

@app.on_event("startup")
def load_model():
    global text_to_video
    try:
        print("Loading model...")
        text_to_video = pipeline(
            task=Tasks.text_to_video_synthesis,
            model='iic/text-to-video-synthesis'
        )
        print("Model loaded successfully!")
    except Exception as e:
        print("Failed to load model:", str(e))
        traceback.print_exc()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate")
async def generate_video(data: PromptRequest):
    global text_to_video
    if text_to_video is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")
    
    try:
        result = text_to_video({'text': data.prompt})
        return {"video_path": result['output_path']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")
