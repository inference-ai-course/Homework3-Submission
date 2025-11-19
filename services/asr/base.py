"""
Abstract ASR Service Interface
"""
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional


class ASRResult(BaseModel):
    """ASR transcription result"""
    text: str
    confidence: Optional[float] = None
    language: Optional[str] = None
    duration: Optional[float] = None


class ASRService(ABC):
    """Abstract base class for ASR services"""
    
    @abstractmethod
    def transcribe(self, audio_path: str) -> ASRResult:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            ASRResult with transcription
        """
        pass
    
    @abstractmethod
    def transcribe_bytes(self, audio_bytes: bytes) -> ASRResult:
        """
        Transcribe audio bytes to text
        
        Args:
            audio_bytes: Audio file content
            
        Returns:
            ASRResult with transcription
        """
        pass
