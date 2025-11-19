"""
FastAPI Application Setup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from api.routes import chat, health
from api.Middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from config.settings import settings
from utils.logger import logger
from utils.file_manager import file_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    
    Startup:
    - Log startup
    - Start cleanup tasks
    
    Shutdown:
    - Clean up resources
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Note: Background tasks would be started here in production
    # For simplicity, we're skipping the cleanup task
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    file_manager.cleanup_old_files()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Voice-enabled AI assistant with ASR, LLM, and TTS",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["Chat"])

# Log registered routes
logger.info("Registered routes:")
for route in app.routes:
    if hasattr(route, "methods"):
        logger.info(f"  {', '.join(route.methods)} {route.path}")
