# MyDigitalTwin Backend API

FastAPI backend for the AI Digital Twin application using Vapi API.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Vapi API Configuration
VAPI_API_KEY=your_vapi_api_key_here
VAPI_BASE_URL=https://api.vapi.ai

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# API Configuration
API_TIMEOUT=30
```

**Important:** Replace `your_vapi_api_key_here` with your actual Vapi API key.

### 3. Run the Server

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API Base: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

## API Endpoints

### Health Check
- `GET /api/health` - Basic health check
- `GET /api/health/vapi` - Vapi API connectivity check

### Text Chat
- `POST /api/chat/text` - Send text message and get AI response
- `GET /api/chat/languages` - Get available languages
- `GET /api/chat/models` - Get available models

### Voice Sessions
- `POST /api/voice/start` - Start a voice session
- `POST /api/voice/stop/{session_id}` - Stop a voice session
- `GET /api/voice/status/{session_id}` - Get voice session status

### Voice Cloning
- `POST /api/voice/clone/upload` - Upload voice sample
- `POST /api/voice/clone/create` - Create voice clone
- `GET /api/voice/clone/status/{clone_id}` - Get clone status
- `POST /api/voice/clone/preview` - Preview voice clone

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   └── cors.py          # CORS middleware
│   ├── services/
│   │   ├── vapi_client.py   # Vapi API client
│   │   └── voice_clone.py   # Voice cloning service
│   ├── routes/
│   │   ├── health.py        # Health check endpoints
│   │   ├── chat.py          # Text chat endpoints
│   │   ├── voice.py         # Voice session endpoints
│   │   └── clone.py         # Voice cloning endpoints
│   └── schemas/
│       ├── chat.py          # Chat request/response models
│       ├── voice.py         # Voice session models
│       └── clone.py         # Voice cloning models
├── .env                     # Environment variables (create this)
└── requirements.txt         # Python dependencies
```

## Testing

You can test the API using:

1. **Swagger UI**: Visit `http://localhost:8000/docs`
2. **Postman**: Import the endpoints and test manually
3. **Frontend**: The HTML files in the `Frontend` directory are already connected

## Notes

- Authentication is currently skipped (no JWT/OAuth)
- All endpoints are publicly accessible
- CORS is configured to allow requests from the frontend
- The backend uses async endpoints for better performance

## Troubleshooting

1. **Import errors**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
2. **Vapi API errors**: Verify your API key is correct in `.env`
3. **CORS errors**: Check that `FRONTEND_URL` in `.env` matches your frontend URL
4. **Port already in use**: Change the port in the uvicorn command or kill the process using port 8000

