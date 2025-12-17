"""
Voice cloning service using Vapi API
"""
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings


class VoiceCloneService:
    """Service for voice cloning operations"""
    
    def __init__(self):
        self.base_url = settings.VAPI_BASE_URL
        self.api_key = settings.VAPI_PRIVATE_KEY.strip() if settings.VAPI_PRIVATE_KEY else ""
        self.timeout = settings.API_TIMEOUT
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
    
    async def upload_voice_sample(
        self,
        audio_file: bytes,
        filename: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Upload a voice sample for cloning"""
        url = f"{self.base_url}/v1/voices"
        
        # Determine content type based on filename extension
        content_type = "audio/mpeg"
        if filename.endswith('.wav'):
            content_type = "audio/wav"
        elif filename.endswith('.m4a'):
            content_type = "audio/m4a"
        elif filename.endswith('.mp3'):
            content_type = "audio/mpeg"
        
        files = {
            "file": (filename, audio_file, content_type)
        }
        data = {}
        if description:
            data["description"] = description
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    headers={"Authorization": self.headers["Authorization"]},
                    files=files,
                    data=data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.content else {"error": str(e)}
                raise Exception(f"Voice upload error: {error_detail}")
            except httpx.RequestError as e:
                raise Exception(f"Upload request failed: {str(e)}")
    
    async def create_voice_clone(
        self,
        voice_sample_id: str,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a voice clone from uploaded sample"""
        url = f"{self.base_url}/v1/voices/{voice_sample_id}/clone"
        
        payload = {}
        if name:
            payload["name"] = name
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    headers={
                        "Authorization": self.headers["Authorization"],
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.content else {"error": str(e)}
                raise Exception(f"Voice clone creation error: {error_detail}")
            except httpx.RequestError as e:
                raise Exception(f"Clone request failed: {str(e)}")
    
    async def get_clone_status(self, clone_id: str) -> Dict[str, Any]:
        """Get the status of a voice clone"""
        url = f"{self.base_url}/v1/voices/{clone_id}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.content else {"error": str(e)}
                raise Exception(f"Status check error: {error_detail}")
            except httpx.RequestError as e:
                raise Exception(f"Status request failed: {str(e)}")
    
    async def preview_voice(
        self,
        voice_id: str,
        text: str
    ) -> Dict[str, Any]:
        """Preview a voice clone with text"""
        url = f"{self.base_url}/v1/voices/{voice_id}/preview"
        
        payload = {"text": text}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    headers={
                        "Authorization": self.headers["Authorization"],
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.content else {"error": str(e)}
                raise Exception(f"Preview error: {error_detail}")
            except httpx.RequestError as e:
                raise Exception(f"Preview request failed: {str(e)}")


# Global service instance
voice_clone_service = VoiceCloneService()

