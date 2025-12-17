# Vapi Web Voice Setup - Quick Fix Guide

## The Error You're Seeing

```
daily-call-object-creation-error
start-method-error
```

This means **your assistant is not configured for web voice** in the Vapi dashboard.

## Quick Fix Steps

### Step 1: Go to Vapi Dashboard

1. Open: https://dashboard.vapi.ai
2. Log in with your account
3. Go to **Assistants** section
4. Find your assistant: `99fb9a3d-f701-494e-9acb-073f9ed4be14`

### Step 2: Configure Assistant for Web Voice

**IMPORTANT**: Your assistant must be configured for **Web/Browser** voice, NOT phone calls.

1. Click on your assistant to edit it
2. Look for **"Voice Type"** or **"Call Type"** setting
3. Make sure it's set to:
   - ✅ **"Web"** or **"Browser"** or **"WebRTC"**
   - ❌ NOT "Phone" or "Outbound"

### Step 3: Required Settings

Your assistant MUST have:

1. ✅ **Model configured** (e.g., GPT-4, Claude, etc.)
2. ✅ **Voice selected** (any voice from the list)
3. ✅ **Voice Type = "Web"** (not phone)
4. ✅ **Assistant is Published/Active**

### Step 4: Verify API Key

1. In Vapi dashboard, go to **Settings** → **API Keys**
2. Copy your **PUBLIC API KEY** (not private)
3. Make sure it matches what's in `voiceChat.html` line 217:
   ```javascript
   const VAPI_PUBLIC_KEY = '34f0859f-e2f6-4fea-a9a9-6d7e0eb28c47';
   ```

### Step 5: Test Again

1. Save your assistant configuration in Vapi dashboard
2. Refresh your `voiceChat.html` page
3. Click the microphone button
4. It should work now!

## If It Still Doesn't Work

### Option A: Create a New Assistant (Recommended)

1. In Vapi dashboard, click **"Create Assistant"**
2. Set it up:
   - Name: "My Digital Twin"
   - Model: GPT-4 or Claude
   - Voice: Choose any voice
   - **Voice Type: Web** (IMPORTANT!)
3. Save and publish
4. Copy the new Assistant ID
5. Update `voiceChat.html` line 218 with the new ID

### Option B: Check Assistant Details

In Vapi dashboard, your assistant should show:
- ✅ Status: Active/Published
- ✅ Voice Type: Web
- ✅ Model: Configured
- ✅ Voice: Selected

## Common Mistakes

❌ **Wrong**: Assistant configured for "Phone" calls  
✅ **Correct**: Assistant configured for "Web" voice

❌ **Wrong**: Using PRIVATE_API_KEY in frontend  
✅ **Correct**: Using PUBLIC_API_KEY in frontend

❌ **Wrong**: Assistant not published  
✅ **Correct**: Assistant is published/active

## Still Having Issues?

1. **Check browser console** - Look for more detailed error messages
2. **Try different browser** - Chrome or Firefox recommended
3. **Check microphone permissions** - Allow microphone access
4. **Verify you're on localhost** - WebRTC needs localhost or HTTPS

## Alternative: Use Vapi Widget (Easier)

If the programmatic approach is too complex, use Vapi's built-in widget which handles everything automatically. See `TROUBLESHOOTING.md` for the widget code.

