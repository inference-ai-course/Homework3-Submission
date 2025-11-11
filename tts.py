"""
Text-to-Speech Module using pyttsx3.

This module provides text-to-speech synthesis functionality for the Voice Assistant System.
"""

import pyttsx3
import tempfile
import os
from typing import Optional


class TTSModule:
    """Text-to-Speech module using pyttsx3 engine."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize TTS engine with pyttsx3.
        
        Args:
            rate: Speech rate (words per minute). Default is 150.
            volume: Volume level (0.0 to 1.0). Default is 0.9.
        """
        print(f"[TTS] TTS Module initialized (rate={rate}, volume={volume})")
        print(f"[TTS] Note: Engine will be created fresh for each synthesis to avoid blocking")
        self.rate = rate
        self.volume = volume
    
    def synthesize(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech and save as audio file.
        
        Args:
            text: Text to synthesize into speech.
            output_path: Optional output file path. If None, creates a temporary file.
            
        Returns:
            str: Path to the generated audio file.
            
        Raises:
            ValueError: If text is empty or None.
            RuntimeError: If speech synthesis fails.
        """
        print(f"[TTS] Starting synthesis: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        if not text or not text.strip():
            print(f"[TTS] ERROR: Empty text provided")
            raise ValueError("Text cannot be empty")
        
        try:
            if output_path is None:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                output_path = temp_file.name
                temp_file.close()
            
            print(f"[TTS] Output path: {output_path}")
            
            # Reinitialize engine for each synthesis to avoid blocking issues
            print(f"[TTS] Creating fresh engine for this request...")
            engine = pyttsx3.init()
            engine.setProperty('rate', self.rate)
            engine.setProperty('volume', self.volume)
            
            # Synthesize speech and save to file
            print(f"[TTS] Saving to file...")
            engine.save_to_file(text, output_path)
            
            print(f"[TTS] Running synthesis...")
            engine.runAndWait()
            
            print(f"[TTS] Stopping engine...")
            engine.stop()
            
            # Verify file was created
            if not os.path.exists(output_path):
                print(f"[TTS] ERROR: Audio file was not created")
                raise RuntimeError("Audio file was not created")
            
            file_size = os.path.getsize(output_path)
            print(f"[TTS] Synthesis complete: {output_path} ({file_size} bytes)")
            return output_path
            
        except ValueError:
            raise
        except Exception as e:
            print(f"[TTS] ERROR: {str(e)}")
            # Clean up temp file if it was created
            if output_path and os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            raise RuntimeError(f"Speech synthesis failed: {str(e)}")


# Global instance for convenience
tts_module = TTSModule()


def synthesize_speech(text: str, output_path: Optional[str] = None) -> str:
    """
    Convenience function for speech synthesis using global TTS module instance.
    
    Args:
        text: Text to synthesize into speech.
        output_path: Optional output file path. If None, creates a temporary file.
        
    Returns:
        str: Path to the generated audio file.
        
    Raises:
        ValueError: If text is empty or None.
        RuntimeError: If speech synthesis fails.
    """
    return tts_module.synthesize(text, output_path)
