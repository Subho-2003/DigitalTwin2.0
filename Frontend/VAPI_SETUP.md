# Vapi Frontend Setup Instructions

## Quick Setup Steps

### 1. Get Your PUBLIC_API_KEY

Your `PUBLIC_API_KEY` is in your backend `.env` file:

Location: `backend/.env`

```env
PUBLIC_API_KEY=your-public-key-here
```

**Copy this value** - you'll need it in the next step.

### 2. Update voiceChat.html

Open `Frontend/voiceChat.html` and find this line (around line 244):

```javascript
const VAPI_PUBLIC_KEY = 'YOUR_PUBLIC_API_KEY_HERE'; // Replace with your PUBLIC_API_KEY from .env
```

**Replace `'YOUR_PUBLIC_API_KEY_HERE'` with your actual PUBLIC_API_KEY.**

Example:
```javascript
const VAPI_PUBLIC_KEY = 'pk-abc123xyz...'; // Your actual public key
```

### 3. Update User ID (Optional)

If you have user authentication, update this line:

```javascript
const DEFAULT_USER_ID = 1; // Replace with actual user ID from your auth system
```

For now, you can:
- Use `1` (default)
- Or create a test user by calling: `POST http://localhost:8000/api/users/create`

### 4. Start Your Backend Server

Make sure your backend is running:

```bash
cd backend
python run.py
```

The server should be running on `http://localhost:8000`

### 5. Open voiceChat.html

You have two options:

#### Option A: Use a Local Server (Recommended)

```bash
# In the Frontend directory
npx serve .
# or
python -m http.server 3000
```

Then open: `http://localhost:3000/voiceChat.html`

#### Option B: Open Directly in Browser

Some browsers may have issues with ES modules. If it doesn't work, use Option A.

### 6. Test the Integration

1. Click the **microphone button** to start voice chat
2. Speak - you should see your transcript appear in real-time
3. The AI will respond
4. Click **stop button** to end the call
5. If "Save to Memory" is checked, the conversation will be saved to your backend

## Troubleshooting

### Error: "Failed to start voice session"

**Check:**
- Did you replace `YOUR_PUBLIC_API_KEY_HERE` with your actual key?
- Is your backend server running?
- Is the PUBLIC_API_KEY correct in your `.env` file?

### Error: "Module not found" or Import Error

**Solution:**
- Use a local server (Option A above) instead of opening the file directly
- Or check that the CDN link is accessible

### Transcript Not Saving

**Check:**
- Is the "Save to Memory" checkbox checked?
- Is your backend server running?
- Check browser console for errors (F12)
- Verify `DEFAULT_USER_ID` exists in your database

### No Voice/Audio

**Check:**
- Browser permissions for microphone access
- Allow microphone when prompted
- Check browser console for errors

## Important Notes

- ✅ **PUBLIC_API_KEY is safe** to expose in frontend code (that's why it's called "public")
- ❌ **Never expose PRIVATE_API_KEY** in frontend
- 🔒 Make sure your backend CORS is configured correctly
- 📝 The transcript is captured automatically during the conversation
- 💾 Conversations are saved to backend only if "Save to Memory" is checked

## Next Steps

1. ✅ Replace PUBLIC_API_KEY in voiceChat.html
2. ✅ Start backend server
3. ✅ Open voiceChat.html in browser
4. ✅ Test voice chat
5. ✅ Verify conversation saves to memory

That's it! Your voice chat should now work with Vapi Web SDK.

