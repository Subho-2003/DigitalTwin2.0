"""
Application configuration
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Vapi API Configuration
    # Note: PUBLIC_KEY is for frontend use only, PRIVATE_KEY for backend (webhooks only)
    VAPI_PUBLIC_KEY: str = os.getenv("PUBLIC_API_KEY", "")
    VAPI_PRIVATE_KEY: str = os.getenv("PRIVATE_API_KEY", "")
    VAPI_ASSISTANT_ID: str = os.getenv("VAPI_ASSISTANT_ID", "")
    VAPI_BASE_URL: str = os.getenv("VAPI_BASE_URL", "https://api.vapi.ai")
    
    # Google Gemini API Configuration (for text chat - FREE)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Frontend Configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # API Configuration
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env file


# Global settings instance
settings = Settings()

