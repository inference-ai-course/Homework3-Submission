"""
Google TTS Service Implementation
"""
from gtts import gTTS
from typing import Optional
from services.tts.base import TTSService, TTSResult
from config.settings import settings
from utils.logger import logger
from utils.file_manager import file_manager
from utils.audio import estimate_audio_duration


class GTTSService(TTSService):
    """Google Text-to-Speech implementation"""
    
    def __init__(
        self,
        language: Optional[str] = None,
        slow: Optional[bool] = None
    ):
        """
        Initialize gTTS service
        
        Args:
            language: Language code (e.g., 'en', 'es', 'fr')
            slow: Whether to use slow speech
        """
        self.language = language or settings.tts_language
        self.slow = slow if slow is not None else settings.tts_slow
        
        logger.info(f"Initialized gTTS service (language: {self.language}, slow: {self.slow})")
    
    def synthesize(self, text: str) -> TTSResult:
        """
        Synthesize text to speech using Google TTS
        
        Args:
            text: Text to convert to speech
            
        Returns:
            TTSResult with audio file path
        """
        try:
            logger.debug(f"Synthesizing text: {text[:50]}...")
            
            # Create gTTS object
            tts = gTTS(
                text=text,
                lang=self.language,
                slow=self.slow
            )
            
            # Generate unique filename
            filename = file_manager.generate_unique_filename(".mp3")
            filepath = file_manager.get_temp_filepath(filename)
            
            # Save audio file
            tts.save(str(filepath))
            
            # Estimate duration
            duration = estimate_audio_duration(text)
            
            logger.info(f"TTS synthesis successful: {filepath}")
            
            return TTSResult(
                audio_path=str(filepath),
                duration=duration,
                format="mp3"
            )
        
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            raise


# Global gTTS instance
gtts_service = GTTSService()
