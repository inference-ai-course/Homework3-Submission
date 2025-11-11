from typing import List, Dict
from dataclasses import dataclass


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation."""
    role: str  # "user" or "assistant"
    text: str


class ConversationManager:
    """Manages conversation history with a sliding window of recent turns."""
    
    def __init__(self, max_history: int = 5):
        """
        Initialize conversation manager.
        
        Args:
            max_history: Maximum number of turns to retain (default: 5)
        """
        self.max_history = max_history
        self.history: List[ConversationTurn] = []
        print(f"[ConversationManager] Initialized with max_history={max_history}")
    
    def add_user_message(self, text: str):
        """Add user message to history."""
        self.history.append(ConversationTurn(role="user", text=text))
        print(f"[ConversationManager] Added user message (total: {len(self.history)} messages)")
        self._trim_history()
    
    def add_assistant_message(self, text: str):
        """Add assistant message to history."""
        self.history.append(ConversationTurn(role="assistant", text=text))
        print(f"[ConversationManager] Added assistant message (total: {len(self.history)} messages)")
        self._trim_history()
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history as list of dicts.
        
        Returns:
            List of dicts with 'role' and 'content' keys
        """
        return [{"role": turn.role, "content": turn.text} for turn in self.history]
    
    def get_prompt_context(self) -> str:
        """
        Build prompt string from recent history.
        
        Returns:
            str: Formatted conversation history for LLM prompt
        """
        recent_turns = self.history[-self.max_history * 2:]
        prompt_lines = []
        for turn in recent_turns:
            prompt_lines.append(f"{turn.role}: {turn.text}")
        return "\n".join(prompt_lines)
    
    def _trim_history(self):
        """
        Keep only the most recent turns.
        Maintains exactly max_history turns = max_history * 2 messages (user + assistant pairs).
        For max_history=5, this keeps the last 10 messages (5 turns).
        """
        if len(self.history) > self.max_history * 2:  # user + assistant = 2 per turn
            old_count = len(self.history)
            self.history = self.history[-(self.max_history * 2):]
            print(f"[ConversationManager] Trimmed history from {old_count} to {len(self.history)} messages (keeping last {self.max_history} turns)")
    
    def clear(self):
        """Clear conversation history."""
        old_count = len(self.history)
        self.history = []
        print(f"[ConversationManager] Cleared history ({old_count} messages removed)")


# Global instance
conversation_manager = ConversationManager()
