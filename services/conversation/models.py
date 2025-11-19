"""
Conversation Data Models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from config.constants import MessageRole


class Message(BaseModel):
    """Single conversation message"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ConversationTurn(BaseModel):
    """Complete conversation turn (user + assistant)"""
    turn_number: int
    user_message: Message
    assistant_message: Message
    asr_confidence: Optional[float] = None
    llm_tokens: Optional[int] = None
    processing_time: Optional[float] = None


class Session(BaseModel):
    """Conversation session"""
    session_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    last_active: datetime = Field(default_factory=datetime.now)
    turns: List[ConversationTurn] = []
    max_turns: int = 5
    
    def add_turn(
        self,
        user_text: str,
        assistant_text: str,
        asr_confidence: Optional[float] = None,
        llm_tokens: Optional[int] = None,
        processing_time: Optional[float] = None
    ):
        """Add a new conversation turn"""
        turn = ConversationTurn(
            turn_number=len(self.turns) + 1,
            user_message=Message(role=MessageRole.USER, content=user_text),
            assistant_message=Message(role=MessageRole.ASSISTANT, content=assistant_text),
            asr_confidence=asr_confidence,
            llm_tokens=llm_tokens,
            processing_time=processing_time
        )
        
        self.turns.append(turn)
        self.last_active = datetime.now()
        
        # Keep only last N turns
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]
    
    def get_history_for_llm(self) -> List[dict]:
        """
        Get conversation history formatted for LLM
        
        Returns:
            List of message dictionaries
        """
        history = []
        for turn in self.turns:
            history.append({
                "role": turn.user_message.role.value,
                "content": turn.user_message.content
            })
            history.append({
                "role": turn.assistant_message.role.value,
                "content": turn.assistant_message.content
            })
        return history
    
    def get_turn_count(self) -> int:
        """Get number of turns in this session"""
        return len(self.turns)
