"""
Startup script for Voice Assistant FastAPI Backend.

This script starts the FastAPI server on port 8000.
"""

import uvicorn

if __name__ == "__main__":
    print("Starting Voice Assistant Backend...")
    print("API will be available at: http://127.0.0.1:8000")
    print("API documentation at: http://127.0.0.1:8000/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "voice_assistant_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
