"""
Health check endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import httpx
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "MyDigitalTwin API"
    }


@router.get("/health/vapi")
async def vapi_health_check():
    """Check Vapi API connectivity"""
    try:
        if not settings.VAPI_PRIVATE_KEY:
            return {
                "status": "not_configured",
                "vapi_status": "private_key_not_set",
                "message": "VAPI_PRIVATE_KEY is optional for webhooks only",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{settings.VAPI_BASE_URL}/v1/health",
                headers={"Authorization": f"Bearer {settings.VAPI_PRIVATE_KEY}"}
            )
            response.raise_for_status()
            return {
                "status": "connected",
                "vapi_status": "healthy",
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "status": "disconnected",
            "vapi_status": "unreachable",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

