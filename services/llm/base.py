"""
Abstract LLM Service Interface
"""
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Optional


class LLMResult(BaseModel):
    """LLM generation result"""
    response: str
    tokens_used: Optional[int] = None
    model_name: Optional[str] = None


class LLMService(ABC):
    """Abstract base class for LLM services"""
    
    @abstractmethod
    def generate(
        self,
        user_message: str,
        conversation_history: Optional[List[dict]] = None
    ) -> LLMResult:
        """
        Generate response to user message
        
        Args:
            user_message: Current user message
            conversation_history: Previous conversation turns
            
        Returns:
            LLMResult with generated response
        """
        pass
