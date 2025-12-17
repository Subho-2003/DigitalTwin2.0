"""
CORS configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI app"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.FRONTEND_URL,
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "file://",  # Allow file:// protocol for local HTML files
            "*"  # Allow all origins for development (remove in production)
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

