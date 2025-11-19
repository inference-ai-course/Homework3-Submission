"""
Voice Agent - Main Entry Point

A real-time voice chatbot that:
- Takes audio input via HTTP
- Transcribes audio to text (ASR with Whisper)
- Generates responses using LLM (Llama 3.2)
- Converts responses to speech (TTS with gTTS)
- Supports 5-turn conversational memory

Usage:
    python main.py

Or with uvicorn directly:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
import uvicorn
from config.settings import settings
from utils.logger import logger


def main():
    """Run the FastAPI application"""
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name}")
    logger.info("=" * 60)
    
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )



if __name__ == "__main__":
    main()
