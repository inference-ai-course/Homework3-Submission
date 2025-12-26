from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import whisper
import torch
import bentoml
import os
import tempfile
from pathlib import Path
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Assistant API")

# Global models and conversation state
asr_model = None
llm_pipeline = None
conversation_history: List[Dict[str, str]] = []

# Configuration
MAX_CONVERSATION_TURNS = 5
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def load_models():
    """Load models on startup"""
    global asr_model, llm_pipeline

    logger.info("Loading Whisper ASR model...")
    asr_model = whisper.load_model("small")

    logger.info("Loading LLM model...")
    try:
        from transformers import pipeline
        # Use a smaller model that fits in 16GB GPU memory
        llm_pipeline = pipeline(
            "text-generation",
            model="meta-llama/Llama-3.2-3B-Instruct",
            device=0 if torch.cuda.is_available() else -1,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        logger.info("Models loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading LLM: {e}")
        logger.info("Falling back to CPU or smaller model...")
        # Fallback to a smaller model or CPU
        llm_pipeline = pipeline(
            "text-generation",
            model="meta-llama/Llama-3.2-1B-Instruct",
            device=-1
        )

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe audio to text using Whisper ASR

    Args:
        audio_bytes: Raw audio file bytes

    Returns:
        Transcribed text
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
    Generate response using LLM with conversation history

    Args:
        user_text: User's transcribed input

    Returns:
        Generated bot response
    """
    global conversation_history

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_text})

    # Keep only last MAX_CONVERSATION_TURNS * 2 messages (user + assistant pairs)
    if len(conversation_history) > MAX_CONVERSATION_TURNS * 2:
        conversation_history = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]

    # Construct prompt from conversation history
    messages = []
    system_message = {
        "role": "system",
        "content": "You are a helpful voice assistant. Provide clear, concise responses suitable for speech."
    }
    messages.append(system_message)
    messages.extend(conversation_history)

    try:
        # Generate response
        outputs = llm_pipeline(
            messages,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            return_full_text=False
        )

        bot_response = outputs[0]["generated_text"].strip()

        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": bot_response})

        logger.info(f"Generated response: {bot_response}")
        return bot_response

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        error_response = "I apologize, but I encountered an error processing your request."
        conversation_history.append({"role": "assistant", "content": error_response})
        return error_response

def synthesize_speech(text: str) -> str:
    """
    Convert text to speech using BentoTTS

    Args:
        text: Text to convert to speech

    Returns:
        Path to generated audio file
    """
    output_path = TEMP_DIR / "response.wav"

    try:
        # Connect to BentoTTS server
        with bentoml.SyncHTTPClient("http://localhost:3000") as client:
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

    Args:
        file: Uploaded audio file from user

    Returns:
        Audio file with bot's voice response
    """
    try:
        # Step 1: Read audio file
        audio_bytes = await file.read()
        logger.info(f"Received audio file: {file.filename}")

        # Step 2: Transcribe audio to text (ASR)
        user_text = transcribe_audio(audio_bytes)

        if not user_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        # Step 3: Generate response using LLM
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
        "llm_loaded": llm_pipeline is not None,
        "cuda_available": torch.cuda.is_available()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
