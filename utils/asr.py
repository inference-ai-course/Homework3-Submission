import os
import logging
import tempfile
import whisper

# load the asr model
asr_model = whisper.load_model("tiny")

def transcribe_audio(audio_bytes, original_filename):
    """
    Accept an audio bytes
    Write it to a temporary file
    transcribe it
    """
    ext = os.path.splitext(original_filename)[1]
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=ext, delete=True) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()  # Ensure data is written

        # Transcribe using Whisper
        result = asr_model.transcribe(temp_audio.name)
        
        return result.get("text", "")