"""
Voice Assistant UI - Gradio Frontend

This module provides a web-based user interface for the Voice Assistant System.
Users can record or upload audio, view conversation history, and listen to responses.
"""

import gradio as gr
import requests
from typing import List, Dict, Tuple, Optional
import tempfile
import os

# Backend API URL
API_URL = "http://127.0.0.1:8000"


def process_audio(audio_file: Optional[str], chat_history: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], Optional[str]]:
    """
    Send audio to backend and update chat history.
    
    Args:
        audio_file: Path to uploaded audio file
        chat_history: Current conversation history
        
    Returns:
        tuple: (updated_chat_history, audio_response_path)
    """
    if audio_file is None:
        return chat_history, None
    
    try:
        # Send audio to backend /chat/ endpoint
        with open(audio_file, "rb") as f:
            files = {"file": ("audio.wav", f, "audio/wav")}
            response = requests.post(f"{API_URL}/chat/", files=files, timeout=150)  # Increased to 150s for 5-turn conversations
        
        if response.status_code == 200:
            # Save response audio to temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            temp_file.write(response.content)
            temp_file.close()
            audio_response = temp_file.name
            
            # Fetch updated conversation history from /history endpoint
            history_response = requests.get(f"{API_URL}/history", timeout=10)
            
            if history_response.status_code == 200:
                history_data = history_response.json()
                updated_history = history_data.get("history", [])
                
                # Convert backend format to Gradio messages format
                chat_history = updated_history
            
            return chat_history, audio_response
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            chat_history.append({"role": "assistant", "content": f"❌ {error_msg}"})
            return chat_history, None
            
    except requests.exceptions.ConnectionError:
        error_msg = "❌ Cannot connect to backend. Please ensure the API server is running on http://127.0.0.1:8000"
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, None
    except requests.exceptions.Timeout:
        error_msg = "❌ Request timed out. The backend may be processing a large request."
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, None
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, None


def clear_conversation() -> Tuple[List[Dict[str, str]], Optional[str]]:
    """
    Clear conversation history on both frontend and backend.
    
    Returns:
        tuple: (empty_chat_history, None for audio)
    """
    print("[Frontend] Clear History button clicked")
    try:
        # Send request to backend to clear conversation state
        print(f"[Frontend] Sending POST request to {API_URL}/clear")
        response = requests.post(f"{API_URL}/clear", timeout=10)
        
        if response.status_code == 200:
            print(f"[Frontend] Backend history cleared successfully")
        else:
            print(f"[Frontend] WARNING: Failed to clear backend history: {response.status_code}")
    except Exception as e:
        print(f"[Frontend] WARNING: Failed to clear backend history: {str(e)}")
    
    # Return empty chat history and None for audio
    print("[Frontend] Returning empty chat history to UI")
    return [], None


def build_ui():
    """
    Build and return the Gradio interface for the Voice Assistant.
    
    Returns:
        gr.Blocks: Configured Gradio Blocks interface
    """
    with gr.Blocks(title="Voice Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎙️ Voice Assistant with Chat History")
        gr.Markdown("Upload audio to chat with the AI assistant. View conversation history below.")
        
        with gr.Row():
            with gr.Column(scale=2):
                # Chat history display
                chatbot = gr.Chatbot(
                    label="Conversation History",
                    type="messages",
                    height=400
                )
                
                # Audio input
                audio_input = gr.Audio(
                    label="Record or Upload Audio",
                    type="filepath",
                    sources=["microphone", "upload"]
                )
                
                # Control buttons
                with gr.Row():
                    submit_btn = gr.Button("Send", variant="primary")
                    clear_btn = gr.Button("Clear History")
                
                # Audio output
                audio_output = gr.Audio(
                    label="Assistant Response",
                    type="filepath",
                    autoplay=True
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### Instructions")
                gr.Markdown("""
                1. Click the microphone to record or upload an audio file
                2. Click 'Send' to process your message
                3. View the conversation history in the chat window
                4. Listen to the assistant's audio response
                5. Click 'Clear History' to start a new conversation
                """)
                
                gr.Markdown("### Status")
                status = gr.Textbox(label="System Status", value="Ready", interactive=False)
        
        # Wire up event handlers
        submit_btn.click(
            fn=process_audio,
            inputs=[audio_input, chatbot],
            outputs=[chatbot, audio_output]
        )
        
        clear_btn.click(
            fn=clear_conversation,
            outputs=[chatbot, audio_output]
        )
    
    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)
