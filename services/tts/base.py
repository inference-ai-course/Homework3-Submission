"""
Abstract TTS Service Interface
"""
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional


class TTSResult(BaseModel):
    """TTS synthesis result"""
    audio_path: str
    duration: Optional[float] = None
    format: str = "mp3"


class TTSService(ABC):
    """Abstract base class for TTS services"""
    
    @abstractmethod
    def synthesize(self, text: str) -> TTSResult:
        """
        Synthesize text to speech
        
        Args:
            text: Text to convert to speech
            
        Returns:
            TTSResult with audio file path
        """
        pass
