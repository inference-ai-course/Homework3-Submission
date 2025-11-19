"""
Application Settings - Centralized configuration management
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    app_name: str = Field(default="Voice Agent", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # API
    api_host: str = Field(default="127.0.0.1", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=True, env="API_RELOAD")
    
    # Models
    whisper_model: str = Field(default="small", env="WHISPER_MODEL")
    whisper_device: str = Field(default="cpu", env="WHISPER_DEVICE")
    
    llm_model: str = Field(
        default="meta-llama/Llama-3.2-1B",
        env="LLM_MODEL"
    )
    llm_device: str = Field(default="cpu", env="LLM_DEVICE")
    llm_max_tokens: int = Field(default=100, env="LLM_MAX_TOKENS")
    
    # TTS
    tts_language: str = Field(default="en", env="TTS_LANGUAGE")
    tts_slow: bool = Field(default=False, env="TTS_SLOW")
    
    # Conversation
    max_conversation_turns: int = Field(default=5, env="MAX_CONVERSATION_TURNS")
    session_timeout: int = Field(default=3600, env="SESSION_TIMEOUT")
    
    # File Settings
    temp_dir: str = Field(default="data/temp", env="TEMP_DIR")
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/voice_agent.log", env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_temp_dir_path(self) -> Path:
        """Get temp directory as Path object and create if doesn't exist"""
        path = Path(self.temp_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def get_log_dir_path(self) -> Path:
        """Get log directory as Path object and create if doesn't exist"""
        path = Path(self.log_file).parent
        path.mkdir(parents=True, exist_ok=True)
        return path


# Global settings instance
settings = Settings()
