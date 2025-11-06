from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from server.src.audio.transcribe import transcribe_audio
from server.src.audio.tts import text_to_speech
from server.src.llm.generate import generate_response

app = FastAPI()

@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    user_text = transcribe_audio(audio_bytes)
    print(user_text)
    bot_text = generate_response(user_text)
    print(bot_text)

    path = "response.wav"
    text_to_speech(bot_text, path)

    return FileResponse(path, media_type="audio/wav")
