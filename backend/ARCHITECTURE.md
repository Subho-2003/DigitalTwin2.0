# Application Architecture

## Overview

This application follows the **correct Vapi architecture** for a college project:

- **Frontend**: Uses Vapi Web SDK for live voice interaction
- **Backend**: Handles memory storage, summaries, and database operations
- **AI**: Uses Google Gemini Flash (FREE) for text chat and summaries

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Vapi Web SDK (@vapi-ai/web)                  │  │
│  │  - Uses PUBLIC_API_KEY (safe to expose)              │  │
│  │  - Handles live voice chat                           │  │
│  │  - Captures transcript in real-time                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          │ Sends transcript after call ends  │
│                          ▼                                   │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ POST /api/memory/save
                          │ {user_id, assistant_id, transcript}
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Memory Save Endpoint                         │  │
│  │  1. Receives transcript from frontend                │  │
│  │  2. Generates summary using Gemini Flash (FREE)      │  │
│  │  3. Stores in SQLite database                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SQLite Database                          │  │
│  │  - users (id, name, email)                           │  │
│  │  - memories (id, user_id, assistant_id,              │  │
│  │             transcript, summary, created_at)         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Frontend (Your HTML/JS Files)

**Responsibilities:**
- Initialize Vapi Web SDK with PUBLIC_API_KEY
- Handle live voice chat
- Capture conversation transcript
- Send transcript to backend after call ends

**Files to Update:**
- `Frontend/voiceChat.html` - Add Vapi Web SDK integration

### 2. Backend (FastAPI)

**Responsibilities:**
- Store conversation transcripts and summaries
- Generate summaries using Gemini Flash (FREE)
- Provide REST API for frontend
- Manage database operations

**Key Endpoints:**
- `POST /api/memory/save` - Save conversation with auto-generated summary
- `GET /api/memory/{user_id}` - Get all memories for a user
- `DELETE /api/memory/{memory_id}` - Delete a memory
- `POST /api/users/create` - Create a user (for demo)
- `GET /api/users/{user_id}` - Get user details
- `POST /api/chat/text` - Text chat using Gemini (fallback)

### 3. Database (SQLite)

**Tables:**

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Memories table
CREATE TABLE memories (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    assistant_id VARCHAR(100) NOT NULL,
    transcript TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Environment Variables

### Backend (.env file)

```env
# Vapi Configuration
PUBLIC_API_KEY=your-public-key-here          # For frontend (safe to expose)
PRIVATE_API_KEY=your-private-key-here        # For backend webhooks only
VAPI_ASSISTANT_ID=99fb9a3d-f701-494e-9acb-073f9ed4be14

# Google Gemini (FREE)
GOOGLE_API_KEY=your-google-api-key-here

# Server Configuration
FRONTEND_URL=http://localhost:3000
API_TIMEOUT=30
```

### Frontend

Make sure to expose `PUBLIC_API_KEY` in your frontend code. It's safe to expose.

## API Keys Explained

| Key | Location | Purpose | Safe to Expose? |
|-----|----------|---------|-----------------|
| PUBLIC_API_KEY | Frontend | Vapi Web SDK initialization | ✅ Yes |
| PRIVATE_API_KEY | Backend only | Webhooks (optional) | ❌ No |
| GOOGLE_API_KEY | Backend only | Text chat & summaries | ❌ No |

## Data Flow

### Voice Conversation Flow:

1. **User clicks "Start Voice Chat"** in frontend
2. **Frontend initializes Vapi Web SDK** with PUBLIC_API_KEY
3. **Vapi handles live voice interaction** (no backend needed)
4. **Frontend captures transcript** as conversation progresses
5. **Call ends** → Frontend sends transcript to `POST /api/memory/save`
6. **Backend generates summary** using Gemini Flash
7. **Backend saves to database** (users + memories tables)
8. **Frontend can fetch memories** via `GET /api/memory/{user_id}`

### Text Chat Flow:

1. **User types message** in frontend
2. **Frontend sends to** `POST /api/chat/text`
3. **Backend uses Gemini Flash** to generate response
4. **Backend returns response** to frontend

## Quick Start

### 1. Set Up Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up .env file with your keys
# Copy from example above

# Run server
python run.py
```

### 2. Set Up Frontend

See `FRONTEND_INTEGRATION.md` for detailed frontend setup.

Key steps:
1. Install `@vapi-ai/web` package
2. Initialize Vapi with PUBLIC_API_KEY
3. Capture transcript during voice chat
4. Send transcript to backend after call ends

### 3. Create Test User

```bash
curl -X POST http://localhost:8000/api/users/create \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'
```

### 4. Test Memory Save

```bash
curl -X POST http://localhost:8000/api/memory/save \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "assistant_id": "99fb9a3d-f701-494e-9acb-073f9ed4be14",
    "transcript": "User: Hello\nAssistant: Hi there! How can I help you?"
  }'
```

## Why This Architecture?

✅ **Correct**: Follows Vapi's recommended architecture  
✅ **Free Tier Friendly**: Uses free Gemini Flash, no phone numbers needed  
✅ **Simple**: Frontend handles voice, backend handles storage  
✅ **Scalable**: Easy to add features later  
✅ **College Project Ready**: Clean, well-documented, academic quality

## Next Steps

1. ✅ Backend is ready
2. ⏳ Update frontend to use Vapi Web SDK (see `FRONTEND_INTEGRATION.md`)
3. ⏳ Test voice chat → memory save flow
4. ⏳ Add UI to display memories
5. ⏳ Add user authentication (optional for demo)

## Support

- **Vapi Docs**: https://docs.vapi.ai
- **Frontend Integration**: See `FRONTEND_INTEGRATION.md`
- **Gemini Setup**: See `GEMINI_SETUP.md`

