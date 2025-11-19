# Create these __init__.py files in each directory:

# config/__init__.py
"""Configuration package"""
from config.settings import settings
from config.constants import *

__all__ = ['settings']

# ============================================

# utils/__init__.py
"""Utilities package"""
from utils.logger import logger
from utils.file_manager import file_manager
from utils.audio_utils import *

__all__ = ['logger', 'file_manager']

# ============================================

# services/__init__.py
"""Services package"""

# ============================================

# services/asr/__init__.py
"""ASR services"""
from services.asr.whisper_asr import whisper_asr

__all__ = ['whisper_asr']

# ============================================

# services/llm/__init__.py
"""LLM services"""
from services.llm.llama_client import llama_llm

__all__ = ['llama_llm']

# ============================================

# services/tts/__init__.py
"""TTS services"""
from services.tts.gtts_client import gtts_service

__all__ = ['gtts_service']

# ============================================

# services/conversation/__init__.py
"""Conversation management"""
from services.conversation.manager import conversation_manager
from services.conversation.models import Session, Message, ConversationTurn

__all__ = ['conversation_manager', 'Session', 'Message', 'ConversationTurn']

# ============================================

# orchestrator/__init__.py
"""Pipeline orchestration"""
from orchestrator.pipeline import voice_pipeline

__all__ = ['voice_pipeline']

# ============================================

# api/__init__.py
"""API package"""

# ============================================

# api/routes/__init__.py
"""API routes"""

# ============================================

# api/middleware/__init__.py
"""API middleware"""

# ============================================

# api/schemas/__init__.py
"""API schemas"""

# ============================================

# tests/__init__.py
"""Test package"""
