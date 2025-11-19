"""
Application Constants
"""
from enum import Enum


class AudioFormat(str, Enum):
    """Supported audio formats"""
    WAV = "audio/wav"
    MP3 = "audio/mpeg"
    OGG = "audio/ogg"
    WEBM = "audio/webm"


class ModelDevice(str, Enum):
    """Device options for model inference"""
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"  # Apple Silicon


class WhisperModelSize(str, Enum):
    """Available Whisper model sizes"""
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class MessageRole(str, Enum):
    """Conversation message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# Supported audio formats for validation
SUPPORTED_AUDIO_FORMATS = [
    AudioFormat.WAV,
    AudioFormat.MP3,
    AudioFormat.OGG,
    AudioFormat.WEBM
]

# Audio file extensions
AUDIO_EXTENSIONS = {
    ".wav": AudioFormat.WAV,
    ".mp3": AudioFormat.MP3,
    ".ogg": AudioFormat.OGG,
    ".webm": AudioFormat.WEBM
}

# Error messages
ERROR_MESSAGES = {
    "invalid_audio_format": "Unsupported audio format. Please upload WAV, MP3, OGG, or WebM files.",
    "file_too_large": "File size exceeds maximum allowed size.",
    "processing_error": "An error occurred while processing your request.",
    "session_not_found": "Session not found. Please create a new session.",
    "asr_error": "Failed to transcribe audio.",
    "llm_error": "Failed to generate response.",
    "tts_error": "Failed to synthesize speech.",
}
