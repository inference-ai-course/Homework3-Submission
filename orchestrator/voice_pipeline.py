"""
Voice Processing Pipeline - Orchestrates ASR, LLM, and TTS
"""
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from pydantic import BaseModel
from pathlib import Path

from services.asr.whisper_asr import whisper_asr
from services.llm.llama_client import llama_llm
from services.tts.gtts_client import gtts_service
from services.conversation.manager import conversation_manager
from utils.logger import logger


class VoiceResponse(BaseModel):
    """Complete voice processing response"""
    audio_path: str
    transcript: str
    bot_response: str
    session_id: str
    processing_time: float
    turn_number: int


class VoicePipeline:
    """Orchestrate the complete voice processing pipeline"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.asr_service = whisper_asr
        self.llm_service = llama_llm
        self.tts_service = gtts_service
        self.conversation_manager = conversation_manager
        
        logger.info("Voice pipeline initialized")
    
    async def run_in_executor(self, func, *args):
        """Run blocking function in thread pool"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args)
    
    async def process(
        self,
        audio_path: Path,
        session_id: Optional[str] = None
    ) -> VoiceResponse:
        """
        Process audio input through complete pipeline
        
        Pipeline:
        1. ASR: Transcribe audio to text
        2. Get conversation history
        3. LLM: Generate response
        4. TTS: Synthesize response to audio
        5. Save conversation turn
        
        Args:
            audio_path: Path to input audio file
            session_id: Optional session ID (creates new if None)
            
        Returns:
            VoiceResponse with results
        """
        start_time = time.time()
        
        logger.info(f"Starting pipeline for session: {session_id}")
        
        try:
            # Get or create session
            session, is_new = self.conversation_manager.get_or_create_session(session_id)
            session_id = session.session_id
            
            if is_new:
                logger.info(f"Created new session: {session_id}")
            
            # Step 1: ASR - Transcribe audio
            logger.debug("Step 1: Running ASR")
            asr_result = await self.run_in_executor(
                self.asr_service.transcribe,
                str(audio_path)
            )
            user_text = asr_result.text
            logger.info(f"ASR completed: '{user_text[:100]}...'")
            
            # Step 2: Get conversation history
            logger.debug("Step 2: Retrieving conversation history")
            history = self.conversation_manager.get_history(session_id)
            logger.debug(f"Retrieved {len(history)} messages from history")
            
            # Step 3: LLM - Generate response
            logger.debug("Step 3: Generating LLM response")
            llm_result = await self.run_in_executor(
                self.llm_service.generate,
                user_text,
                history
            )
            bot_text = llm_result.response
            logger.info(f"LLM completed: '{bot_text[:100]}...'")
            
            # Step 4: TTS - Synthesize response
            logger.debug("Step 4: Synthesizing speech")
            tts_result = await self.run_in_executor(
                self.tts_service.synthesize,
                bot_text
            )
            output_audio_path = tts_result.audio_path
            logger.info(f"TTS completed: {output_audio_path}")
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Step 5: Save conversation turn
            logger.debug("Step 5: Saving conversation turn")
            self.conversation_manager.add_turn(
                session_id=session_id,
                user_text=user_text,
                assistant_text=bot_text,
                asr_confidence=asr_result.confidence,
                llm_tokens=llm_result.tokens_used,
                processing_time=processing_time
            )
            
            turn_number = session.get_turn_count()
            
            logger.info(
                f"Pipeline completed in {processing_time:.2f}s "
                f"(Turn {turn_number}/{session.max_turns})"
            )
            
            return VoiceResponse(
                audio_path=output_audio_path,
                transcript=user_text,
                bot_response=bot_text,
                session_id=session_id,
                processing_time=processing_time,
                turn_number=turn_number
            )
        
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise


# Global pipeline instance
voice_pipeline = VoicePipeline()
