from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import whisper

app = FastAPI()

asr_model = whisper.load_model("small")

def transcribe_audio(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = asr_model.transcribe("temp.wav")
    return result["text"]

@app.post("/chat")
async def chat_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    user_text = transcribe_audio(audio_bytes)
    print(user_text)
    # TODO: ASR → LLM → TTS
    return FileResponse("response.wav", media_type="audio/wav")