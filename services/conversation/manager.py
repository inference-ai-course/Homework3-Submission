"""
Conversation State Manager
"""
import uuid
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from services.conversation.models import Session
from config.settings import settings
from utils.logger import logger


class ConversationManager:
    """Manage conversation sessions and state"""
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.max_turns = settings.max_conversation_turns
        self.session_timeout = settings.session_timeout
    
    def create_session(self) -> str:
        """
        Create a new conversation session
        
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id,
            max_turns=self.max_turns
        )
        self.sessions[session_id] = session
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get existing session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session object or None if not found
        """
        session = self.sessions.get(session_id)
        
        if session:
            # Check if session expired
            time_inactive = (datetime.now() - session.last_active).total_seconds()
            if time_inactive > self.session_timeout:
                logger.info(f"Session {session_id} expired")
                del self.sessions[session_id]
                return None
        
        return session
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> tuple[Session, bool]:
        """
        Get existing session or create new one
        
        Args:
            session_id: Optional session identifier
            
        Returns:
            Tuple of (Session, is_new)
        """
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session, False
        
        # Create new session
        new_id = self.create_session()
        return self.sessions[new_id], True
    
    def add_turn(
        self,
        session_id: str,
        user_text: str,
        assistant_text: str,
        asr_confidence: Optional[float] = None,
        llm_tokens: Optional[int] = None,
        processing_time: Optional[float] = None
    ) -> bool:
        """
        Add conversation turn to session
        
        Args:
            session_id: Session identifier
            user_text: User's message
            assistant_text: Assistant's response
            asr_confidence: ASR confidence score
            llm_tokens: Number of tokens used
            processing_time: Time taken to process
            
        Returns:
            True if successful, False otherwise
        """
        session = self.get_session(session_id)
        if not session:
            logger.error(f"Session not found: {session_id}")
            return False
        
        session.add_turn(
            user_text=user_text,
            assistant_text=assistant_text,
            asr_confidence=asr_confidence,
            llm_tokens=llm_tokens,
            processing_time=processing_time
        )
        
        logger.debug(f"Added turn to session {session_id}. Total turns: {session.get_turn_count()}")
        return True
    
    def get_history(self, session_id: str, max_turns: Optional[int] = None) -> List[dict]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session identifier
            max_turns: Maximum number of turns to return
            
        Returns:
            List of conversation messages
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        history = session.get_history_for_llm()
        
        if max_turns and len(history) > max_turns * 2:  # *2 because each turn has user+assistant
            history = history[-(max_turns * 2):]
        
        return history
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired = []
        
        for session_id, session in self.sessions.items():
            time_inactive = (current_time - session.last_active).total_seconds()
            if time_inactive > self.session_timeout:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def get_active_session_count(self) -> int:
        """Get number of active sessions"""
        return len(self.sessions)


# Global conversation manager instance
conversation_manager = ConversationManager()
