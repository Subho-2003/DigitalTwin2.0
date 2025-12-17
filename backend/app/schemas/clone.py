"""
Voice cloning request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class VoiceCloneUploadResponse(BaseModel):
    """Voice sample upload response schema"""
    voice_sample_id: str = Field(..., description="Uploaded voice sample ID")
    status: str = Field(..., description="Upload status")
    filename: str = Field(..., description="Uploaded filename")


class VoiceCloneCreateRequest(BaseModel):
    """Voice clone creation request schema"""
    voice_sample_id: str = Field(..., description="Voice sample ID to clone")
    name: Optional[str] = Field(None, description="Name for the voice clone")


class VoiceCloneCreateResponse(BaseModel):
    """Voice clone creation response schema"""
    clone_id: str = Field(..., description="Created clone ID")
    status: str = Field(..., description="Clone status")
    estimated_time_seconds: Optional[int] = Field(None, description="Estimated processing time")


class VoiceCloneStatusResponse(BaseModel):
    """Voice clone status response schema"""
    clone_id: str = Field(..., description="Clone ID")
    status: str = Field(..., description="Current status (processing, ready, failed)")
    progress_percent: Optional[float] = Field(None, description="Processing progress (0-100)")
    error: Optional[str] = Field(None, description="Error message if failed")


class VoicePreviewRequest(BaseModel):
    """Voice preview request schema"""
    voice_id: str = Field(..., description="Voice ID to preview")
    text: str = Field(..., description="Text to synthesize")


class VoicePreviewResponse(BaseModel):
    """Voice preview response schema"""
    audio_url: str = Field(..., description="URL to preview audio")
    duration_seconds: float = Field(..., description="Audio duration")

