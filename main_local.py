from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import whisper
import bentoml
import os
import tempfile
from pathlib import Path
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Assistant API (Local LLM)")

# Global models and conversation state
asr_model = None
conversation_history: List[Dict[str, str]] = []

# Configuration
MAX_CONVERSATION_TURNS = 5
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

# --- NEW CONFIGURATION ---
# URL for your local LLM service (e.g., Ollama, or a local BentoML service)
LLM_SERVICE_URL = "http://localhost:11434" # Ollama's default port

@app.on_event("startup")
async def load_models():
    """Load models on startup (Only ASR model remains internal)"""
    global asr_model

    logger.info("Loading Whisper ASR model...")
    # NOTE: Keep the whisper model loading internal as it is lightweight.
    asr_model = whisper.load_model("small")
    logger.info("ASR model loaded successfully. LLM is configured for external service.")

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe audio to text using Whisper ASR
    """
    temp_audio_path = TEMP_DIR / "temp_input.wav"

    try:
        # Save audio bytes to temporary file
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        # Transcribe using Whisper
        result = asr_model.transcribe(str(temp_audio_path))
        transcribed_text = result["text"].strip()

        logger.info(f"Transcribed: {transcribed_text}")
        return transcribed_text

    finally:
        # Cleanup temp file
        if temp_audio_path.exists():
            temp_audio_path.unlink()

def generate_response(user_text: str) -> str:
    """
    Generate response using local LLM service with conversation history
    """
    global conversation_history
    LLM_SYSTEM_PROMPT = "You are a helpful voice assistant named Llama 3.2. Provide clear, concise responses suitable for speech."

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_text})

    # Keep only last MAX_CONVERSATION_TURNS * 2 messages (user + assistant pairs)
    if len(conversation_history) > MAX_CONVERSATION_TURNS * 2:
        conversation_history = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]

    # --- NEW PROMPT CONSTRUCTION FOR LLM API ---
    # Construct a simplified prompt string from the history (User: X, Assistant: Y, User: Z)
    prompt_parts = [LLM_SYSTEM_PROMPT]
    for turn in conversation_history:
        role = turn["role"].capitalize()
        content = turn["content"]
        prompt_parts.append(f"{role}: {content}")

    # The final prompt sent to the LLM will ask it to respond as the Assistant
    final_prompt = "\n".join(prompt_parts) + "\nAssistant:"
    # --- END NEW PROMPT CONSTRUCTION ---

    try:
        # Connect to the external LLM service using bentoml client
        with bentoml.SyncHTTPClient(LLM_SERVICE_URL) as client:
            # Assuming the local LLM service has a standard 'generate' or 'chat' endpoint
            # We are configuring for Ollama's /api/generate endpoint payload structure here.
            
            # NOTE: You MUST change this payload and endpoint if your local LLM is NOT Ollama.
            payload = {
                "model": "llama3.2:latest", # The local model name you specified
                "prompt": final_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 150
                }
            }
            
            # Ollama uses the /api/generate endpoint and returns JSON
            outputs = client.generate(**payload) 
            
            # Assuming the output structure has a 'response' field for the text
            bot_response = outputs.get("response", "").strip() 
            
        if not bot_response:
             raise ValueError("LLM returned an empty response.")

        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": bot_response})

        logger.info(f"Generated response: {bot_response}")
        return bot_response

    except Exception as e:
        logger.error(f"Error generating response from local LLM service: {e}")
        error_response = f"I apologize, but I encountered an error communicating with the local LLM service at {LLM_SERVICE_URL}. Please check the server status."
        conversation_history.append({"role": "assistant", "content": error_response})
        return error_response

def synthesize_speech(text: str) -> str:
    """
    Convert text to speech using BentoTTS
    """
    # NOTE: TTS service URL remains http://localhost:3000 as in original code
    output_path = TEMP_DIR / "response.wav"

    try:
        # Connect to BentoTTS server
        with bentoml.SyncHTTPClient("http://localhost:3000") as client:
            # Assuming a 'synthesize' endpoint for the TTS service
            result = client.synthesize(
                text=text,
                lang="en"
            )

        # Save the audio response
        with open(output_path, "wb") as f:
            f.write(result)

        logger.info(f"Speech synthesized: {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Error synthesizing speech: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"TTS service error: {str(e)}. Make sure BentoTTS server is running on http://localhost:3000"
        )

@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    """
    Main chat endpoint - handles full voice interaction pipeline
    """
    try:
        # Step 1: Read audio file
        audio_bytes = await file.read()
        logger.info(f"Received audio file: {file.filename}")

        # Step 2: Transcribe audio to text (ASR)
        user_text = transcribe_audio(audio_bytes)

        if not user_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        # Step 3: Generate response using local LLM service
        bot_text = generate_response(user_text)

        # Step 4: Convert response to speech (TTS)
        audio_path = synthesize_speech(bot_text)

        # Step 5: Return audio file
        return FileResponse(
            audio_path,
            media_type="audio/wav",
            filename="response.wav"
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # Use a user-friendly 500 message
        if "Please check the server status" in str(e):
            raise HTTPException(status_code=503, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation")
async def get_conversation():
    """Get current conversation history"""
    return {
        "history": conversation_history,
        "turn_count": len(conversation_history) // 2
    }

@app.post("/reset")
async def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    logger.info("Conversation history reset")
    return {"message": "Conversation reset successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "asr_loaded": asr_model is not None,
        # LLM health now depends on the external service being up
        "llm_external": True,
        "llm_service_url": LLM_SERVICE_URL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)