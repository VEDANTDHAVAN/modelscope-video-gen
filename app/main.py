from fastapi import FastAPI
from pydantic import BaseModel
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

# Load the pipeline
text_to_video = pipeline(Tasks.text_to_video_synthesis, model='iic/text-to-video-synthesis')

@app.post("/generate")
async def generate_video(data: PromptRequest):
    result = text_to_video({'text': data.prompt})
    return {"video_path": result['output_path']}
