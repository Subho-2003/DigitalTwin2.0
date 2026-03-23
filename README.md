# MyDigitalTwin - Complete Setup Guide

This guide will help you set up and run both the frontend and backend of the MyDigitalTwin application.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- A Vapi API key (get one from https://vapi.ai)

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Environment File

Create a `.env` file in the `backend` directory:

```env
VAPI_API_KEY=your_actual_vapi_api_key_here
VAPI_BASE_URL=https://api.vapi.ai
FRONTEND_URL=http://localhost:3000
API_TIMEOUT=30
```

**Important:** Replace `your_actual_vapi_api_key_here` with your real Vapi API key.

### 4. Run the Backend Server

```bash
# Option 1: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using the run script
python run.py
```

The backend will start at `http://localhost:8000`

You can verify it's working by visiting:
- `http://localhost:8000/api/health` - Health check
- `http://localhost:8000/docs` - Interactive API documentation

## Frontend Setup

### Option 1: Using Python HTTP Server (Recommended)

```bash
# From the project root directory
cd Frontend
python -m http.server 3000
```

Then open your browser and navigate to:
- `http://localhost:3000/index.html` - Landing page
- `http://localhost:3000/login.html` - Login page
- `http://localhost:3000/dashboard.html` - Dashboard
- `http://localhost:3000/textChat.html` - Text chat
- `http://localhost:3000/voiceChat.html` - Voice chat
- `http://localhost:3000/voiceCloning.html` - Voice cloning

### Option 2: Using Node.js HTTP Server

If you have Node.js installed:

```bash
# Install http-server globally (one time)
npm install -g http-server

# Run the server
cd Frontend
http-server -p 3000
```

### Option 3: Using VS Code Live Server

If you're using VS Code:
1. Install the "Live Server" extension
2. Right-click on any HTML file
3. Select "Open with Live Server"

## Connecting Frontend to Backend

The frontend is already configured to connect to the backend at `http://localhost:8000`.

If your backend runs on a different port, update the `API_BASE_URL` in each HTML file:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Change port if needed
```

## Testing the Application

### 1. Test Text Chat

1. Open `http://localhost:3000/textChat.html`
2. Type a message in the input field
3. Click the send button or press Enter
4. The AI response should appear in the chat

### 2. Test Voice Chat

1. Open `http://localhost:3000/voiceChat.html`
2. Click the microphone button to start a voice session
3. The session will connect to the backend
4. Click stop to end the session

### 3. Test Voice Cloning

1. Open `http://localhost:3000/voiceCloning.html`
2. Either:
   - Upload an audio file (MP3, WAV, M4A)
   - Or click "Start Recording" to record your voice
3. Click "Deploy Voice" to create the clone
4. Wait for processing to complete

## API Endpoints

All endpoints are available at `http://localhost:8000/api`:

### Health
- `GET /api/health` - Basic health check
- `GET /api/health/vapi` - Vapi connectivity check

### Chat
- `POST /api/chat/text` - Send text message
- `GET /api/chat/languages` - Get available languages
- `GET /api/chat/models` - Get available models

### Voice
- `POST /api/voice/start` - Start voice session
- `POST /api/voice/stop/{session_id}` - Stop voice session
- `GET /api/voice/status/{session_id}` - Get session status

### Voice Cloning
- `POST /api/voice/clone/upload` - Upload voice sample
- `POST /api/voice/clone/create` - Create voice clone
- `GET /api/voice/clone/status/{clone_id}` - Get clone status
- `POST /api/voice/clone/preview` - Preview voice

## Troubleshooting

### Backend Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Vapi API errors**: 
   - Verify your API key is correct in `.env`
   - Check that `VAPI_BASE_URL` is correct
   - Ensure you have internet connectivity

3. **Port already in use**: 
   - Change the port in the uvicorn command
   - Or kill the process using port 8000

### Frontend Issues

1. **CORS errors**: 
   - Make sure you're serving the HTML files through a web server (not file://)
   - Check that `FRONTEND_URL` in backend `.env` matches your frontend URL
   - Verify backend CORS settings allow your frontend origin

2. **API connection errors**:
   - Verify backend is running on port 8000
   - Check browser console for error messages
   - Ensure `API_BASE_URL` in HTML files matches backend URL

3. **Voice recording not working**:
   - Check browser permissions for microphone access
   - Use HTTPS or localhost (some browsers require secure context)

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── core/                 # Configuration
│   │   ├── services/             # API clients
│   │   ├── routes/               # API endpoints
│   │   └── schemas/              # Data models
│   ├── .env                      # Environment variables (create this)
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
├── Frontend/
│   ├── index.html               # Landing page
│   ├── login.html                # Login page
│   ├── dashboard.html            # Dashboard
│   ├── textChat.html             # Text chat interface
│   ├── voiceChat.html            # Voice chat interface
│   ├── voiceCloning.html         # Voice cloning interface
│   ├── settings.html             # Settings page
│   └── userProfilr.html          # User profile
└── SETUP.md                      # This file
```

## Next Steps

1. **Get a Vapi API Key**: Sign up at https://vapi.ai and get your API key
2. **Configure Backend**: Add your API key to the `.env` file
3. **Start Backend**: Run the backend server
4. **Start Frontend**: Serve the HTML files through a web server
5. **Test**: Try out all the features!

## Notes

- Authentication is currently skipped (no login required)
- All endpoints are publicly accessible
- The backend uses async endpoints for better performance
- CORS is configured to allow requests from the frontend

## Support

For issues or questions:
1. Check the browser console for errors
2. Check the backend logs for API errors
3. Verify all environment variables are set correctly
4. Ensure both frontend and backend are running

