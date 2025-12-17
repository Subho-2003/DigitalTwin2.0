# Troubleshooting Voice Chat Issues

## Error: "daily-call-object-creation-error"

This error means Vapi couldn't create a WebRTC connection via Daily.co. Here's how to fix it:

### Step 1: Check Assistant Configuration in Vapi Dashboard

1. Go to your Vapi dashboard: https://dashboard.vapi.ai
2. Navigate to your assistant (ID: `99fb9a3d-f701-494e-9acb-073f9ed4be14`)
3. Check the assistant settings:
   - **Voice Type**: Should be set to "Web" or "Browser" (NOT "Phone")
   - **Model**: Should be configured (e.g., GPT-4, Claude, etc.)
   - **Voice**: Should have a voice selected

### Step 2: Verify Your API Keys

1. Check your `.env` file in the `backend` folder:
   ```
   PUBLIC_API_KEY=34f0859f-e2f6-4fea-a9a9-6d7e0eb28c47
   PRIVATE_API_KEY=your-private-key
   VAPI_ASSISTANT_ID=99fb9a3d-f701-494e-9acb-073f9ed4be14
   ```

2. Make sure `PUBLIC_API_KEY` in your `.env` matches the one in `voiceChat.html` (line 217)

### Step 3: Check Browser Permissions

1. **Microphone Access**: 
   - Click the lock icon in your browser's address bar
   - Make sure microphone is set to "Allow"
   - Refresh the page and try again

2. **HTTPS/Localhost**:
   - WebRTC requires HTTPS or localhost
   - Make sure you're accessing via `http://localhost:3000` (not `file://`)
   - Use a local server (see below)

### Step 4: Test with a Simple Example

Try this minimal test in browser console:

```javascript
import('https://cdn.skypack.dev/@vapi-ai/web').then(async (module) => {
    const Vapi = module.default;
    const vapi = new Vapi('34f0859f-e2f6-4fea-a9a9-6d7e0eb28c47');
    
    vapi.on('error', (err) => console.error('Error:', err));
    vapi.on('call-start', () => console.log('Started!'));
    
    await vapi.start('99fb9a3d-f701-494e-9acb-073f9ed4be14');
});
```

### Step 5: Common Issues

**Issue**: Assistant not configured for web voice
- **Fix**: In Vapi dashboard, edit your assistant and ensure it's set for "Web" voice, not phone

**Issue**: Wrong API key
- **Fix**: Make sure you're using PUBLIC_API_KEY (starts with `pk-` or similar), not PRIVATE_API_KEY

**Issue**: Assistant ID doesn't exist
- **Fix**: Verify the assistant ID in your Vapi dashboard matches the one in the code

**Issue**: Browser blocking WebRTC
- **Fix**: Try a different browser (Chrome/Firefox recommended)
- Check browser console for WebRTC errors

### Step 6: Alternative: Use Vapi Widget (Easier)

If the programmatic approach isn't working, you can use Vapi's built-in widget:

```html
<script>
  var vapiInstance = null;
  const assistant = "99fb9a3d-f701-494e-9acb-073f9ed4be14";
  const apiKey = "34f0859f-e2f6-4fea-a9a9-6d7e0eb28c47";
  
  (function (d, t) {
    var g = document.createElement(t),
      s = d.getElementsByTagName(t)[0];
    g.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
    g.defer = true;
    g.async = true;
    s.parentNode.insertBefore(g, s);
    g.onload = function () {
      vapiInstance = window.vapiSDK.run({
        apiKey: apiKey,
        assistant: assistant,
      });
    };
  })(document, "script");
</script>
```

This creates a floating button widget that handles everything automatically.

## Still Not Working?

1. Check Vapi dashboard for any error messages
2. Verify your assistant is published/active
3. Check browser console for detailed error messages
4. Try creating a new assistant in Vapi dashboard
5. Contact Vapi support with your assistant ID and error details

