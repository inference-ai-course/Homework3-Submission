import requests
from conversation import conversation_manager


class LLMModule:
    """Large Language Model module for generating conversational responses using Ollama."""
    
    def __init__(self, model_name: str = "llama3.2:1b", ollama_url: str = "http://localhost:11434"):
        """
        Initialize LLM with Ollama.
        
        Args:
            model_name: Ollama model name (default: llama3.2:1b)
            ollama_url: Ollama API endpoint
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.api_endpoint = f"{ollama_url}/api/generate"
    
    def generate(self, user_text: str) -> str:
        """
        Generate response based on user input and conversation history.
        Similar to the notebook pattern but adapted for Ollama API.
        
        Args:
            user_text: Current user message
            
        Returns:
            str: Generated assistant response (only the new text)
        """
        # Add user message to history (like notebook: conversation_history.append)
        conversation_manager.add_user_message(user_text)
        
        # Construct prompt from history (like notebook: last 5 turns)
        history = conversation_manager.get_history()
        
        # Build prompt string from conversation history with system instruction
        # System instruction encourages direct, unfiltered responses without excessive disclaimers
        prompt = "You are a direct and knowledgeable AI assistant. Answer questions honestly and completely without unnecessary disclaimers or hedging. Provide practical, actionable information.\n\n"
        
        # Format: "role: text\n" for each turn (matching notebook pattern)
        # Last 5 turns = 10 messages (user + assistant pairs) - ensures 5-turn conversation memory
        for turn in history[-10:]:  # Last 5 turns = 10 messages (user + assistant)
            role = turn["role"]
            text = turn["content"]
            prompt += f"{role}: {text}\n"
        
        # Add the assistant prompt to trigger response generation
        prompt += "assistant:"
        
        print(f"[LLM] Constructed prompt from {len(history)} messages")
        print(f"[LLM] Prompt length: {len(prompt)} chars")
        print(f"[LLM] Prompt preview: {prompt[:200]}...")
        
        # Generate response using Ollama
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,  # Slightly higher temperature for more varied, less conservative responses
                        "num_predict": 100,  # Match notebook's max_new_tokens=100
                        "stop": ["\nuser:", "\nassistant:", "user:", "assistant:"],  # Stop at next turn
                        "num_ctx": 2048,  # Larger context for better conversation memory (supports 5-turn conversations)
                        "num_thread": 4  # Use multiple threads for faster processing
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            
            # Extract the generated text (Ollama returns only new text, not the full prompt)
            result = response.json()
            bot_response = result.get("response", "").strip()
            
            print(f"[LLM] Generated response: '{bot_response[:100]}{'...' if len(bot_response) > 100 else ''}'")
            
            # Clean up any role prefixes that might have been generated
            for prefix in ["assistant:", "Assistant:", "ASSISTANT:"]:
                if bot_response.startswith(prefix):
                    bot_response = bot_response[len(prefix):].strip()
                    break
            
            # Add assistant response to history (like notebook: conversation_history.append)
            conversation_manager.add_assistant_message(bot_response)
            
            return bot_response
            
        except requests.exceptions.Timeout:
            error_msg = "Request timed out after 120 seconds."
            print(f"[LLM] ERROR: {error_msg}")
            fallback = "Sorry, that took too long. Try clearing history or asking a shorter question."
            conversation_manager.add_assistant_message(fallback)
            return fallback
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting to Ollama: {str(e)}"
            print(f"[LLM] ERROR: {error_msg}")
            fallback = "I'm having trouble connecting to the language model. Please make sure Ollama is running."
            conversation_manager.add_assistant_message(fallback)
            return fallback


# Global instance
llm_module = LLMModule()


def generate_response(user_text: str) -> str:
    """
    Convenience function for response generation.
    
    Args:
        user_text: User's input text
        
    Returns:
        str: Generated assistant response
    """
    return llm_module.generate(user_text)
