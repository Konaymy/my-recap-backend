from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import edge_tts
import os

app = FastAPI()

# Lovable Frontend မှ လာသော Request များကို ခွင့်ပြုရန် CORS သတ်မှတ်ခြင်း
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice: str = "my-MM-NilarNeural"  # မြန်မာ မလေးအသံ (အမျိုးသားအသံအတွက် "my-MM-ThihaNeural")

@app.get("/")
def home():
    return {"status": "Backend Server is running successfully!"}

@app.post("/generate-audio")
async def generate_audio(request: TTSRequest):
    output_file = "recap_audio.mp3"
    try:
        communicate = edge_tts.Communicate(request.text, request.voice)
        await communicate.save(output_file)
        return FileResponse(output_file, media_type="audio/mpeg", filename="recap_audio.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
