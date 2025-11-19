"""
Chat Endpoint - Main Voice Interaction
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path

from api.Schemas.schemas import ChatResponse, ErrorResponse
from orchestrator.voice_pipeline import voice_pipeline
from utils.file_manager import file_manager
from utils.audio import validate_audio_format, format_file_size
from config.settings import settings
from config.constants import ERROR_MESSAGES
from utils.logger import logger

router = APIRouter()


@router.get("/chat/")
async def chat_get_info():
    """
    Chat endpoint information
    
    This endpoint only accepts POST requests with an audio file.
    Use the /docs endpoint to see the API documentation and test the endpoint.
    """
    return {
        "error": "Method Not Allowed",
        "message": "This endpoint only accepts POST requests with an audio file.",
        "usage": {
            "method": "POST",
            "endpoint": "/chat/",
            "content_type": "multipart/form-data",
            "required_field": "file (audio file: WAV, MP3, OGG, WebM)",
            "optional_header": "X-Session-ID (for conversation continuity)"
        },
        "documentation": "/docs",
        "test_script": "Use quick_test.py to test this endpoint"
    }


@router.post(
    "/chat/",
    response_class=FileResponse,
    responses={
        200: {
            "content": {"audio/mpeg": {}},
            "description": "Audio response with metadata in headers"
        },
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def chat_endpoint(
    file: UploadFile = File(..., description="Audio file (WAV, MP3, OGG, WebM)"),
    session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """
    Voice chat endpoint
    
    Process audio input and return audio response:
    1. Receive audio file
    2. Transcribe audio (ASR)
    3. Generate response (LLM)
    4. Synthesize speech (TTS)
    5. Return audio file
    
    **Headers:**
    - X-Session-ID (optional): Session identifier for conversation continuity
    
    **Response Headers:**
    - X-Session-ID: Session identifier
    - X-Transcript: User's transcribed text
    - X-Bot-Response: Assistant's response text
    - X-Turn-Number: Current conversation turn
    - X-Processing-Time: Total processing time (seconds)
    """
    input_audio_path = None
    output_audio_path = None
    
    try:
        # Validate file format
        if not validate_audio_format(file.filename):
            raise HTTPException(
                status_code=400,
                detail=ERROR_MESSAGES["invalid_audio_format"]
            )
        
        # Read file content
        audio_bytes = await file.read()
        file_size = len(audio_bytes)
        
        # Validate file size
        if file_size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"{ERROR_MESSAGES['file_too_large']} "
                       f"(Uploaded: {format_file_size(file_size)}, "
                       f"Max: {format_file_size(settings.max_file_size)})"
            )
        
        logger.info(
            f"Received audio file: {file.filename} "
            f"({format_file_size(file_size)}) "
            f"Session: {session_id or 'new'}"
        )
        
        # Save uploaded file
        input_audio_path = await file_manager.save_uploaded_file(
            audio_bytes,
            filename=None  # Auto-generate
        )
        
        # Process through pipeline
        response = await voice_pipeline.process(
            audio_path=input_audio_path,
            session_id=session_id
        )
        
        output_audio_path = Path(response.audio_path)
        
        # Prepare response headers
        # Clean header values to ensure they're valid HTTP header values
        # HTTP headers must be encodable in latin-1 (only ASCII + extended ASCII)
        def clean_header_value(value: str) -> str:
            """Clean header value to ensure it's valid HTTP header (latin-1 encodable)"""
            if not value:
                return ""
            # Convert to string if not already
            if not isinstance(value, str):
                value = str(value)
            
            # Remove or replace non-ASCII characters
            # Keep only ASCII printable characters (32-126) and common whitespace
            cleaned = ""
            for char in value:
                code = ord(char)
                # Keep ASCII printable characters (32-126) and tab/newline (9, 10)
                if 32 <= code <= 126 or code in (9, 10, 13):
                    cleaned += char
                elif code > 127:
                    # Replace non-ASCII characters with '?' or remove them
                    # For better readability, we'll replace with space
                    cleaned += " "
                # Skip other control characters
            
            # Replace newlines and carriage returns with spaces
            cleaned = cleaned.replace("\n", " ").replace("\r", " ").replace("\t", " ")
            
            # Collapse multiple spaces into one
            cleaned = " ".join(cleaned.split())
            
            # Ensure it can be encoded in latin-1
            try:
                cleaned.encode('latin-1')
            except UnicodeEncodeError:
                # If still can't encode, remove all non-ASCII
                cleaned = cleaned.encode('ascii', errors='ignore').decode('ascii')
            
            # Limit length to avoid header size issues (HTTP headers typically max 8192 bytes)
            if len(cleaned.encode('latin-1')) > 4000:
                cleaned = cleaned[:4000] + "..."
            
            return cleaned
        
        headers = {
            "X-Session-ID": response.session_id,
            "X-Transcript": clean_header_value(response.transcript),
            "X-Bot-Response": clean_header_value(response.bot_response),
            "X-Turn-Number": str(response.turn_number),
            "X-Processing-Time": f"{response.processing_time:.2f}"
        }
        
        logger.info(
            f"Returning response - Session: {response.session_id}, "
            f"Turn: {response.turn_number}, "
            f"Time: {response.processing_time:.2f}s"
        )
        
        # Return audio file
        return FileResponse(
            path=output_audio_path,
            media_type="audio/mpeg",
            filename=f"response_{response.turn_number}.mp3",
            headers=headers
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"{ERROR_MESSAGES['processing_error']}: {str(e)}"
        )
    
    finally:
        # Clean up input file (output file managed by FileResponse)
        if input_audio_path and input_audio_path.exists():
            file_manager.delete_file(input_audio_path)
