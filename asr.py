import whisper
import tempfile
import os


class ASRModule:
    def __init__(self, model_size: str = "small"):
        """
        Initialize Whisper ASR model.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        print(f"[ASR] Loading Whisper model (size: {model_size})...")
        self.model = whisper.load_model(model_size)
        print(f"[ASR] Whisper model loaded successfully")
    
    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio bytes to text.
        
        Args:
            audio_bytes: Raw audio data in bytes
            
        Returns:
            str: Transcribed text
            
        Raises:
            Exception: On transcription failure
        """
        print(f"[ASR] Starting transcription ({len(audio_bytes)} bytes)")
        temp_path = None
        try:
            # Write to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name
            
            print(f"[ASR] Temp file created: {temp_path}")
            
            # Transcribe audio
            result = self.model.transcribe(temp_path)
            transcribed_text = result["text"].strip()
            
            print(f"[ASR] Transcription complete: '{transcribed_text}'")
            return transcribed_text
            
        except Exception as e:
            print(f"[ASR] ERROR: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
            
        finally:
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                    print(f"[ASR] Temp file cleaned up")
                except Exception:
                    pass  # Ignore cleanup errors


# Global instance
asr_module = ASRModule()


def transcribe_audio(audio_bytes: bytes) -> str:
    """Convenience function for transcription."""
    return asr_module.transcribe(audio_bytes)
