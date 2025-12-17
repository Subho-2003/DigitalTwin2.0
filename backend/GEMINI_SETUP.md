# Google Gemini API Setup (FREE)

## Quick Setup Guide

### 1. Get Your Free Google API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Add to .env File

Add this line to your `backend/.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with the API key you just copied.

### 3. Install Dependencies

Run this command in your backend directory:

```bash
pip install google-generativeai==0.3.2
```

Or if you're in a virtual environment:

```bash
.\venv\Scripts\activate
pip install google-generativeai==0.3.2
```

### 4. Restart Your Server

After adding the API key, restart your backend server.

## Benefits

- **100% FREE** - No credit card required
- **Gemini Flash** - Fast and efficient
- **No usage limits** for reasonable usage
- **Works immediately** - No approval needed

## Example .env File

```
VAPI_API_KEY=d34bc97d-60dc-4cec-b51a-3d640773f167
VAPI_ASSISTANT_ID=99fb9a3d-f701-494e-9acb-073f9ed4be14
VAPI_BASE_URL=https://api.vapi.ai
GOOGLE_API_KEY=your_google_api_key_here
FRONTEND_URL=http://localhost:3000
API_TIMEOUT=30
```

That's it! Your text chat will now use the free Gemini Flash model.

