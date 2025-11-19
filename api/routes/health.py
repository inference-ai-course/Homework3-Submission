"""
Health Check Endpoint
"""
from fastapi import APIRouter
from api.Schemas.schemas import HealthResponse
from config.settings import settings
from services.conversation.manager import conversation_manager

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns service status and basic metrics
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        active_sessions=conversation_manager.get_active_session_count()
    )


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Voice Agent API",
        "version": settings.app_version,
        "endpoints": {
            "health": "/health",
            "chat": "/chat/",
            "docs": "/docs"
        }
    }
