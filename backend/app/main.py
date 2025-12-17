"""
FastAPI main application entry point
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cors import setup_cors
from app.routes import health, chat, voice, clone, webhook, memory, users
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="MyDigitalTwin API",
    description="AI Digital Twin backend using Vapi API",
    version="1.0.0"
)

# Setup CORS
setup_cors(app)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])
app.include_router(clone.router, prefix="/api/voice/clone", tags=["Voice Clone"])
app.include_router(webhook.router, tags=["Webhook"])  # No prefix - webhook at root level
app.include_router(memory.router, prefix="/api/memory", tags=["Memory"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.on_event("startup")
async def startup_event():
    # Initialize database - create tables if they don't exist
    init_db()
    print("🚀 Vapi backend ready")
    print("📡 API endpoints available at /api")
    print("🗄️  Database initialized: digital_twin.db")
    print("🔗 Webhook endpoint: POST /vapi/webhook")


@app.get("/")
async def root():
    return {
        "message": "MyDigitalTwin API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def root_health_check():
    """Root-level health check endpoint (alias for /api/health)"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "MyDigitalTwin API"
    }

