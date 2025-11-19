"""
Audio Processing Utilities
"""
from pathlib import Path
from typing import Optional
import math


def estimate_audio_duration(text: str, words_per_minute: int = 150) -> float:
    """
    Estimate audio duration based on text length
    
    Args:
        text: Text to estimate
        words_per_minute: Average speaking rate
        
    Returns:
        Estimated duration in seconds
    """
    word_count = len(text.split())
    duration_minutes = word_count / words_per_minute
    duration_seconds = duration_minutes * 60
    return max(1.0, duration_seconds)  # Minimum 1 second


def validate_audio_format(filename: str) -> bool:
    """
    Validate if file extension is supported
    
    Args:
        filename: Name of the audio file
        
    Returns:
        True if valid, False otherwise
    """
    from config.constants import AUDIO_EXTENSIONS
    
    extension = Path(filename).suffix.lower()
    return extension in AUDIO_EXTENSIONS


def get_audio_format(filename: str) -> Optional[str]:
    """
    Get MIME type from filename
    
    Args:
        filename: Name of the audio file
        
    Returns:
        MIME type or None
    """
    from config.constants import AUDIO_EXTENSIONS
    
    extension = Path(filename).suffix.lower()
    return AUDIO_EXTENSIONS.get(extension)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"
