"""
Voice cloning endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional

from app.schemas.clone import (
    VoiceCloneUploadResponse,
    VoiceCloneCreateRequest,
    VoiceCloneCreateResponse,
    VoiceCloneStatusResponse,
    VoicePreviewRequest,
    VoicePreviewResponse
)
from app.services.voice_clone import voice_clone_service

router = APIRouter()


@router.post("/upload", response_model=VoiceCloneUploadResponse)
async def upload_voice_sample(
    file: UploadFile = File(...),
    description: Optional[str] = None
):
    """Upload a voice sample for cloning"""
    try:
        # Read file content
        audio_content = await file.read()
        
        # Upload to Vapi
        response = await voice_clone_service.upload_voice_sample(
            audio_file=audio_content,
            filename=file.filename,
            description=description
        )
        
        return VoiceCloneUploadResponse(
            voice_sample_id=response.get("id", response.get("voice_sample_id", "")),
            status=response.get("status", "uploaded"),
            filename=file.filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload voice sample: {str(e)}"
        )


@router.post("/create", response_model=VoiceCloneCreateResponse)
async def create_voice_clone(request: VoiceCloneCreateRequest):
    """Create a voice clone from uploaded sample"""
    try:
        response = await voice_clone_service.create_voice_clone(
            voice_sample_id=request.voice_sample_id,
            name=request.name
        )
        
        return VoiceCloneCreateResponse(
            clone_id=response.get("id", response.get("clone_id", "")),
            status=response.get("status", "processing"),
            estimated_time_seconds=response.get("estimated_time_seconds")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create voice clone: {str(e)}"
        )


@router.get("/status/{clone_id}", response_model=VoiceCloneStatusResponse)
async def get_clone_status(clone_id: str):
    """Get the status of a voice clone"""
    try:
        response = await voice_clone_service.get_clone_status(clone_id)
        
        return VoiceCloneStatusResponse(
            clone_id=clone_id,
            status=response.get("status", "unknown"),
            progress_percent=response.get("progress_percent"),
            error=response.get("error")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get clone status: {str(e)}"
        )


@router.post("/preview", response_model=VoicePreviewResponse)
async def preview_voice(request: VoicePreviewRequest):
    """Preview a voice clone with text"""
    try:
        response = await voice_clone_service.preview_voice(
            voice_id=request.voice_id,
            text=request.text
        )
        
        return VoicePreviewResponse(
            audio_url=response.get("audio_url", ""),
            duration_seconds=response.get("duration_seconds", 0.0)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to preview voice: {str(e)}"
        )

