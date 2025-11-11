"""
Startup script for Voice Assistant Gradio Frontend.

This script starts the Gradio UI on port 7860.
"""

import sys
import subprocess

if __name__ == "__main__":
    print("Starting Voice Assistant Frontend...")
    print("UI will be available at: http://127.0.0.1:7860")
    print("\nMake sure the backend is running on port 8000!")
    print("Press CTRL+C to stop the server\n")
    
    # Run the Gradio UI
    subprocess.run([sys.executable, "voice_assistant_ui.py"])
