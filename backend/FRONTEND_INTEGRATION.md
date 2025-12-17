# Frontend Integration Guide

## Overview

Your application now follows the correct Vapi architecture:
- **Frontend**: Uses Vapi Web SDK for live voice chat
- **Backend**: Handles memory storage and summaries using Gemini AI

## Architecture

```
Frontend (Browser)
├── Vapi Web SDK (@vapi-ai/web)
│   ├── Uses PUBLIC_API_KEY (safe to expose)
│   ├── Handles live voice interaction
│   └── Captures transcript in real-time
└── Sends transcript to backend after call ends

Backend (FastAPI)
├── Receives transcript from frontend
├── Generates summary using Gemini Flash (FREE)
└── Stores in SQLite database
```

## Step 1: Install Vapi Web SDK

In your frontend project:

```bash
npm install @vapi-ai/web
```

Or if using vanilla HTML/JS, use CDN:

```html
<script src="https://unpkg.com/@vapi-ai/web@latest/dist/index.js"></script>
```

## Step 2: Initialize Vapi in Frontend

### Using ES Modules:

```javascript
import Vapi from "@vapi-ai/web";

// Get your PUBLIC_API_KEY from .env (safe to expose)
const vapi = new Vapi(import.meta.env.VITE_VAPI_PUBLIC_KEY);
// Or hardcode: const vapi = new Vapi("your-public-key-here");
```

### Using CDN:

```html
<script type="module">
  const vapi = new Vapi("your-public-key-here");
</script>
```

## Step 3: Start Voice Chat

```javascript
// Your assistant ID from Vapi dashboard
const ASSISTANT_ID = "99fb9a3d-f701-494e-9acb-073f9ed4be14";

// Store transcript as conversation progresses
let fullTranscript = [];

function startVoice() {
  vapi.start(ASSISTANT_ID);
  
  // Clear transcript when new call starts
  fullTranscript = [];
}

function stopVoice() {
  vapi.stop();
}
```

## Step 4: Capture Transcript

```javascript
// Listen for messages (transcripts)
vapi.on("message", (msg) => {
  if (msg.type === "transcript") {
    // Build full conversation transcript
    const transcriptEntry = `${msg.role}: ${msg.transcript}\n`;
    fullTranscript.push(transcriptEntry);
    
    // Optional: Display in UI
    console.log(msg.role, msg.transcript);
  }
});

// Listen for call events
vapi.on("call-start", () => {
  console.log("Call started");
  // Update UI to show "listening" state
});

vapi.on("call-end", async () => {
  console.log("Call ended");
  
  // Send transcript to backend for saving
  await saveConversationToBackend();
});
```

## Step 5: Save Conversation to Backend

```javascript
async function saveConversationToBackend() {
  // Combine all transcript entries
  const transcriptText = fullTranscript.join("");
  
  // Get current user ID (you should have this from your auth system)
  const userId = getCurrentUserId(); // Replace with your user ID logic
  
  if (!transcriptText || transcriptText.trim().length === 0) {
    console.log("No transcript to save");
    return;
  }
  
  try {
    const response = await fetch("http://localhost:8000/api/memory/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        assistant_id: "99fb9a3d-f701-494e-9acb-073f9ed4be14",
        transcript: transcriptText
      })
    });
    
    const result = await response.json();
    
    if (response.ok) {
      console.log("Memory saved successfully:", result);
      // Show success message to user
    } else {
      console.error("Failed to save memory:", result);
    }
  } catch (error) {
    console.error("Error saving memory:", error);
  }
}
```

## Step 6: Fetch User Memories

```javascript
async function loadUserMemories(userId) {
  try {
    const response = await fetch(`http://localhost:8000/api/memory/${userId}`);
    const data = await response.json();
    
    if (response.ok) {
      console.log("Memories loaded:", data.memories);
      // Display memories in UI
      displayMemories(data.memories);
    }
  } catch (error) {
    console.error("Error loading memories:", error);
  }
}

function displayMemories(memories) {
  // Example: Display in a list
  memories.forEach(memory => {
    console.log(`
      Summary: ${memory.summary}
      Date: ${new Date(memory.created_at).toLocaleDateString()}
      ---
    `);
  });
}
```

## Complete Example

```javascript
import Vapi from "@vapi-ai/web";

const vapi = new Vapi("your-public-api-key");
const ASSISTANT_ID = "99fb9a3d-f701-494e-9acb-073f9ed4be14";
const API_BASE_URL = "http://localhost:8000/api";

let fullTranscript = [];

// Initialize event listeners
vapi.on("call-start", () => {
  console.log("Call started");
  fullTranscript = []; // Reset transcript
});

vapi.on("call-end", async () => {
  console.log("Call ended");
  await saveConversation();
});

vapi.on("message", (msg) => {
  if (msg.type === "transcript") {
    fullTranscript.push(`${msg.role}: ${msg.transcript}\n`);
  }
});

// Start/Stop functions
export function startVoice() {
  vapi.start(ASSISTANT_ID);
}

export function stopVoice() {
  vapi.stop();
}

// Save conversation
async function saveConversation() {
  const transcript = fullTranscript.join("");
  if (!transcript.trim()) return;
  
  try {
    const res = await fetch(`${API_BASE_URL}/memory/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: 1, // Get from your auth system
        assistant_id: ASSISTANT_ID,
        transcript
      })
    });
    
    const data = await res.json();
    console.log("Saved:", data);
  } catch (error) {
    console.error("Save error:", error);
  }
}
```

## Important Notes

1. **PUBLIC_API_KEY is safe** - It's designed to be exposed in frontend code
2. **PRIVATE_API_KEY stays in backend** - Never expose this in frontend
3. **User ID** - You need to implement user authentication/login to get user_id
4. **CORS** - Make sure your backend allows requests from your frontend domain
5. **API URL** - Update `API_BASE_URL` to match your backend URL

## Environment Variables

### Frontend (.env or similar):

```env
VITE_VAPI_PUBLIC_KEY=your-public-key-here
VITE_API_BASE_URL=http://localhost:8000
```

### Backend (.env):

```env
PUBLIC_API_KEY=your-public-key-here
PRIVATE_API_KEY=your-private-key-here
VAPI_ASSISTANT_ID=99fb9a3d-f701-494e-9acb-073f9ed4be14
GOOGLE_API_KEY=your-google-api-key-here
```

## Next Steps

1. Set up user authentication to get user_id
2. Test voice chat with Vapi Web SDK
3. Test memory saving after call ends
4. Display memories in your UI
5. Add memory deletion functionality

That's it! Your frontend now handles live voice, and your backend handles memory storage.

