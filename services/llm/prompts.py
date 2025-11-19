"""
LLM Prompt Templates
"""

SYSTEM_PROMPT = """You are a helpful voice assistant. You provide clear, concise, and natural-sounding responses.

Guidelines:
- Keep responses conversational and friendly
- Be concise but informative (aim for 2-3 sentences unless more detail is needed)
- Speak naturally as if having a voice conversation
- Use simple language that sounds good when spoken aloud
- Avoid long lists, complex formatting, or technical jargon unless specifically asked
- If you don't know something, admit it honestly
"""

CONVERSATION_TEMPLATE = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|>
{conversation_history}
<|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

"""


def build_prompt(
    user_message: str,
    conversation_history: list = None,
    system_prompt: str = SYSTEM_PROMPT
) -> str:
    """
    Build prompt for LLM from conversation components
    
    Args:
        user_message: Current user message
        conversation_history: List of previous messages
        system_prompt: System instruction
        
    Returns:
        Formatted prompt string
    """
    # Build conversation history
    history_text = ""
    if conversation_history:
        for msg in conversation_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_text += f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>\n"
    
    # Build complete prompt
    prompt = CONVERSATION_TEMPLATE.format(
        system_prompt=system_prompt,
        conversation_history=history_text,
        user_message=user_message
    )
    
    return prompt
