# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

from app.asr import transcribe_audio
from app.tts import synthesize_speech
from app.llm import generate_response

app = FastAPI()

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temporary file directory
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# Mount static files
STATIC_DIR = Path("static")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def read_root():
    """Serve the main HTML file"""
    return FileResponse("index.html", media_type="text/html")

@app.post("/chat/")
async def chat_endpoint(audio: UploadFile = File(...)):
    """
    Voice chat endpoint
    1. Receive audio file
    2. Transcribe to text (ASR)
    3. Generate response (LLM)
    4. Synthesize speech (TTS)
    5. Return JSON with transcribed text, response text, and audio
    """
    audio_path = None
    try:
        # Save uploaded audio file with .wav extension
        audio_path = TEMP_DIR / "input_audio.wav"
        content = await audio.read()
        with open(audio_path, "wb") as f:
            f.write(content)
        
        print(f"[CHAT] Saved audio to: {audio_path}")
        
        # 1. ASR: Audio -> Text
        print("[CHAT] Transcribing audio...")
        user_text = transcribe_audio(str(audio_path))
        print(f"[CHAT] Transcribed: {user_text}")
        
        # 2. LLM: Generate response
        print("[CHAT] Generating response...")
        bot_response = generate_response(user_text)
        print(f"[CHAT] Response: {bot_response}")
        
        # 3. TTS: Text -> Audio
        print("[CHAT] Synthesizing speech...")
        output_path = TEMP_DIR / "output.wav"
        synthesize_speech(bot_response, str(output_path))
        print(f"[CHAT] Synthesized to: {output_path}")
        
        # 4. Read audio file and return with text
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
        
        # Return JSON response with text and audio data
        import base64
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return {
            "user_text": user_text,
            "bot_response": bot_response,
            "audio": audio_b64
        }
    
    except Exception as e:
        import traceback
        print(f"[CHAT ERROR] {str(e)}")
        traceback.print_exc()
        return {"error": str(e)}
    
    finally:
        # Clean up temporary files
        if audio_path and audio_path.exists():
            audio_path.unlink()

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}