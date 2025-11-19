"""
Whisper ASR Service Implementation
"""
import whisper
import tempfile
from pathlib import Path
from typing import Optional
from services.asr.base import ASRService, ASRResult
from config.settings import settings
from utils.logger import logger
from utils.file_manager import file_manager


class WhisperASRService(ASRService):
    """OpenAI Whisper ASR implementation"""
    
    def __init__(
        self,
        model_size: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize Whisper ASR service
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Device to use (cpu, cuda)
        """
        self.model_size = model_size or settings.whisper_model
        self.device = device or settings.whisper_device
        
        logger.info(f"Loading Whisper model: {self.model_size} on {self.device}")
        self.model = whisper.load_model(self.model_size, device=self.device)
        logger.info("Whisper model loaded successfully")
    
    def transcribe(self, audio_path: str) -> ASRResult:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            ASRResult with transcription
        """
        try:
            logger.debug(f"Transcribing audio file: {audio_path}")
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_path,
                fp16=False if self.device == "cpu" else True
            )
            
            text = result.get("text", "").strip()
            language = result.get("language", "unknown")
            
            logger.info(f"Transcription successful. Language: {language}, Text length: {len(text)}")
            
            return ASRResult(
                text=text,
                language=language,
                confidence=None  # Whisper doesn't provide word-level confidence by default
            )
        
        except Exception as e:
            logger.error(f"ASR transcription failed: {e}")
            raise
    
    def transcribe_bytes(self, audio_bytes: bytes) -> ASRResult:
        """
        Transcribe audio bytes to text
        
        Args:
            audio_bytes: Audio file content
            
        Returns:
            ASRResult with transcription
        """
        # Save bytes to temporary file
        temp_filename = file_manager.generate_unique_filename(".wav")
        temp_path = file_manager.get_temp_filepath(temp_filename)
        
        try:
            # Write bytes to file
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
            
            # Transcribe the file
            result = self.transcribe(str(temp_path))
            
            return result
        
        finally:
            # Clean up temp file
            file_manager.delete_file(temp_path)


# Global Whisper ASR instance
whisper_asr = WhisperASRService()
