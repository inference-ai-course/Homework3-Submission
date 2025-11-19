"""
API Response Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    active_sessions: int


class ChatResponse(BaseModel):
    """Chat endpoint response"""
    session_id: str = Field(..., description="Session identifier")
    transcript: str = Field(..., description="Transcribed user text")
    bot_response: str = Field(..., description="Assistant's response text")
    turn_number: int = Field(..., description="Current turn number")
    processing_time: float = Field(..., description="Total processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123-def456-ghi789",
                "transcript": "What's the weather like today?",
                "bot_response": "I don't have access to real-time weather data, but you can check your local weather service for current conditions.",
                "turn_number": 1,
                "processing_time": 8.5
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "processing_error",
                "detail": "Failed to transcribe audio"
            }
        }
