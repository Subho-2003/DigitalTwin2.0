"""
Chat request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Text chat request schema"""
    message: str = Field(..., description="User message")
    language: Optional[str] = Field(None, description="Language code (e.g., 'en', 'es')")
    model: Optional[str] = Field(None, description="Model to use")


class ChatResponse(BaseModel):
    """Text chat response schema"""
    response: str = Field(..., description="AI response")
    latency_ms: float = Field(..., description="Response latency in milliseconds")
    model_used: Optional[str] = Field(None, description="Model used for response")
    language: Optional[str] = Field(None, description="Language detected/used")
    
    class Config:
        # Disable protected namespace warning for "model_used" field
        protected_namespaces = ()

