from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import whisper
from transformers import pipeline
import sys

# CosyVoice root
sys.path.insert(0, r".\CosyVoice")
# Matcha-TTS folder
sys.path.insert(0, r".\CosyVoice\third_party\Matcha-TTS")

from cosyvoice.cli.cosyvoice import CosyVoice, CosyVoice2
from cosyvoice.utils.file_utils import load_wav
import os, asyncio, torchaudio

# Initialize FastAPI app
app = FastAPI()

# Load Whisper ASR model
asr_model = whisper.load_model("small")

# LLM Respose
llm = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0") 

# Initialize TTS model
LOCAL_MODEL_DIR = r"./homework/Week 3/pretrained_models/CosyVoice2-0.5B"
cosyvoice = CosyVoice2(model_dir=LOCAL_MODEL_DIR, load_jit=False)
prompt_speech_16k = load_wav('./asset/zero_shot_prompt.wav', 16000)

# Store conversations 
conversations = {}
#conversation_history = []

@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...), session_id: str = "default"):
    # Initialize conversation history for this session
    if session_id not in conversations:
        conversations[session_id] = []
    
    conversation_history = conversations[session_id] 
  
    # Read upload audio
    audio_bytes = await file.read()

    # ASR → LLM → TTS

    # Save temporarily and transcribe
    temp_file = f"temp_{session_id}.wav"
    try:
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)
        result = asr_model.transcribe(temp_file)
        user_text = result["text"]
    finally:
        # clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    print(f"User said: {user_text}")

    # Generate LLM response
    conversation_history.append({"role": "user", "text": user_text})
    
    def generate_response(user_text):
        conversation_history.append({"role": "user", "text": user_text})
        # Construct prompt from history
        prompt = ""
        for turn in conversation_history[-5:]:
            prompt += f"{turn['role']}: {turn['text']}\n"
        outputs = llm(prompt, max_new_tokens=100)
        generated = outputs[0]["generated_text"] 
        bot_response = generated[len(prompt):].strip() 
        conversation_history.append({"role": "assistant", "text": bot_response})
        return bot_response

    bot_text = generate_response(user_text)
    print(f"Bot response: {bot_text}")

    async def synthesize_speech(text: str, voice_profile: str = "neutral") -> str:
        out_dir = "tts_outputs"
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, f"{voice_profile}_response.wav")

        loop = asyncio.get_event_loop()

        # Personalize voice tone per speaker
        voice_prompts = {
            "women": "women's voice",
            "man": "man's voice",
            "neutral": "neutral"
        }

        def _run_tts():
            for i, j in enumerate(
                cosyvoice.inference_zero_shot(
                    text,
                    voice_prompts.get(voice_profile, "neutral"),
                    prompt_speech_16k,
                    stream=False
                )
            ):
                torchaudio.save(output_path, j["tts_speech"], cosyvoice.sample_rate)

        await loop.run_in_executor(None, _run_tts)
        return output_path


    audio_path = await synthesize_speech(bot_text)

    return FileResponse(audio_path, media_type="audio/wav")

