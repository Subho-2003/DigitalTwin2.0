"""
Text chat endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import time

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.openai_client import openai_client

router = APIRouter()


@router.post("/text", response_model=ChatResponse)
async def send_text_message(request: ChatRequest):
    """Send a text message and get AI response"""
    start_time = time.time()
    
    try:
        # Use OpenAI API for text chat (Vapi focuses on voice)
        response = await openai_client.send_message(
            message=request.message,
            language=request.language,
            model=request.model
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        return ChatResponse(
            response=response.get("response", response.get("message", "No response available")),
            latency_ms=round(latency_ms, 2),
            model_used=response.get("model", request.model),
            language=response.get("language", request.language)
        )
    except Exception as e:
        # Even if there's an error, provide a helpful response
        latency_ms = (time.time() - start_time) * 1000
        error_detail = str(e)
        return ChatResponse(
            response=f"Hey, I got your message but ran into an issue: {error_detail}. Please check your Google Gemini API key (GOOGLE_API_KEY) in the .env file.",
            latency_ms=round(latency_ms, 2),
            model_used=request.model,
            language=request.language
        )


@router.get("/languages")
async def get_languages():
    """Get available languages"""
    # Return default languages
    languages = [
        {"code": "en", "name": "English"},
        {"code": "es", "name": "Spanish"},
        {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},
        {"code": "hi", "name": "Hindi"},
        {"code": "ja", "name": "Japanese"},
        {"code": "zh", "name": "Chinese"},
    ]
    return {"languages": languages}


@router.get("/models")
async def get_models():
    """Get available models"""
    # Return Gemini models (all free)
    models = [
        {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash (FREE)"},
        {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro (FREE)"},
        {"id": "gemini-pro", "name": "Gemini Pro (FREE)"},
    ]
    return {"models": models}

