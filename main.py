from fastapi import FastAPI, Response, UploadFile, File
from fastapi.responses import FileResponse
from response_generation import generate_response
from transcribe_audio import transcribe_audio

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    user_text = transcribe_audio(audio_bytes)
    print(user_text)
    generated_text = generate_response(user_text)
    print(generated_text)
    # TODO: ASR → LLM → TTS
    return Response("")