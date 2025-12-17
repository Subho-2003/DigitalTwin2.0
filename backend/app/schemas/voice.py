"""
Voice session request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class VoiceSessionRequest(BaseModel):
    """Voice session start request schema"""
    language: Optional[str] = Field(None, description="Language code")
    voice_id: Optional[str] = Field(None, description="Voice ID to use")


class VoiceSessionResponse(BaseModel):
    """Voice session response schema"""
    session_id: str = Field(..., description="Session ID")
    status: str = Field(..., description="Session status")
    websocket_url: Optional[str] = Field(None, description="WebSocket URL for real-time communication")


class VoiceStatusResponse(BaseModel):
    """Voice session status response schema"""
    session_id: str = Field(..., description="Session ID")
    status: str = Field(..., description="Current status")
    duration_seconds: Optional[float] = Field(None, description="Session duration")

