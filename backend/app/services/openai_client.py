"""
Google Gemini API client for text chat functionality (FREE)
Using Gemini Flash which is free to use - using Python SDK like working version
"""
import asyncio
from typing import Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Try to import google.generativeai - will fail gracefully if not installed
try:
    import google.generativeai as genai
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False
    logger.warning("google.generativeai not installed. Install with: pip install google-generativeai")


class OpenAIClient:
    """Client for Google Gemini API text chat (using Gemini Flash - FREE)"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY.strip() if settings.GOOGLE_API_KEY else ""
        # Try gemini-2.5-flash first (from working version), fallback to gemini-1.5-flash
        self.model_name = "gemini-2.5-flash"  # Use the model from working version
        self.timeout = settings.API_TIMEOUT
        
        if self.api_key and GEMINI_SDK_AVAILABLE:
            genai.configure(api_key=self.api_key)
            logger.info("Google Gemini API key configured (using Python SDK with gemini-2.5-flash)")
        else:
            if not self.api_key:
                logger.warning("GOOGLE_API_KEY is not set - text chat will use fallback")
            if not GEMINI_SDK_AVAILABLE:
                logger.warning("google.generativeai SDK not installed - install with: pip install google-generativeai")
    
    async def send_message(
        self,
        message: str,
        model: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a text message to Gemini Flash and get response"""
        
        if not self.api_key:
            # Fallback response when Gemini is not configured
            return {
                "response": f"I received your message: '{message}'. Google Gemini API is not configured. Please add GOOGLE_API_KEY to your .env file for free AI-powered text chat. Get your free API key from: https://makersuite.google.com/app/apikey",
                "model": model or "fallback",
                "language": language or "en"
            }
        
        if not GEMINI_SDK_AVAILABLE:
            return {
                "response": f"I received your message: '{message}'. Please install google-generativeai package: pip install google-generativeai",
                "model": model or "error",
                "language": language or "en"
            }
        
        try:
            # Use the model from working version (gemini-2.5-flash) or requested model
            requested_model = model or self.model_name
            
            # Get available models first and use exact names from the list
            available_models = []
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                logger.info(f"Available Gemini models: {available_models[:5]}")
            except Exception as e:
                logger.warning(f"Could not list models: {e}")
            
            # Build list of model names to try - use EXACT names from available models list
            model_names_to_try = []
            
            # Priority order for models to try
            preferred_models = [
                'models/gemini-2.5-flash',  # Best - newest and fastest
                'models/gemini-2.0-flash-exp',  # Experimental but good
                'models/gemini-2.5-pro',  # Pro version
                'models/gemini-1.5-flash',  # Fallback
                'models/gemini-1.5-pro',  # Pro fallback
                'models/gemini-pro'  # Old fallback
            ]
            
            if available_models:
                # Use exact model names from available models list
                # Try requested model first
                if requested_model in available_models:
                    model_names_to_try.append(requested_model)
                elif f'models/{requested_model}' in available_models:
                    model_names_to_try.append(f'models/{requested_model}')
                
                # Then try preferred models in order (if they're available)
                for preferred in preferred_models:
                    if preferred in available_models and preferred not in model_names_to_try:
                        model_names_to_try.append(preferred)
                
                # If still nothing, use first available model
                if not model_names_to_try and available_models:
                    model_names_to_try.append(available_models[0])
            else:
                # Fallback if we can't list models - try common names
                model_names_to_try = [
                    'models/gemini-2.5-flash',
                    f'models/{requested_model}',
                    requested_model,
                    'models/gemini-1.5-flash'
                ]
            
            gemini_model = None
            last_error = None
            
            # Try each model name until one works
            for model_name_attempt in model_names_to_try:
                try:
                    logger.info(f"Attempting to initialize model: {model_name_attempt}")
                    gemini_model = genai.GenerativeModel(model_name_attempt)
                    logger.info(f"Successfully initialized model: {model_name_attempt}")
                    break
                except Exception as e:
                    last_error = e
                    logger.debug(f"Model {model_name_attempt} failed: {e}")
                    continue
            
            if not gemini_model:
                raise Exception(f"Could not initialize any Gemini model. Tried: {model_names_to_try}. Last error: {last_error}")
            
            # Use the working model
            model = gemini_model
            
            # Prepare the prompt with human-like persona
            # Make it respond like a real person, not an AI bot
            system_instruction = """You are a real human being having a natural conversation. 
- Respond naturally and conversationally, like you're texting a friend
- Don't mention that you're an AI, assistant, or bot
- Use casual language, contractions, and natural expressions
- Show personality, opinions, and emotions
- Don't be overly formal or robotic
- Use "I", "me", "my" - speak from your own perspective
- Be genuine and authentic, like a real person would respond
- Keep responses concise and natural, not essay-like
- If asked about being AI, deflect naturally like a human would"""
            
            if language and language != "en":
                system_instruction += f"\n\nPlease respond in {language}."
            
            # Build the full prompt
            full_prompt = f"{system_instruction}\n\nUser: {message}\n\nAssistant:"
            
            # Generate response using SDK (run in executor to make it async-friendly)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": 0.9,  # Higher temperature for more natural, varied responses
                        "top_k": 40,
                        "top_p": 0.95,
                        "max_output_tokens": 512,  # Shorter responses for more natural conversation
                    }
                )
            )
            
            if response and response.text:
                ai_response = response.text.strip()
                return {
                    "response": ai_response,
                    "model": requested_model,
                    "language": language or "en"
                }
            else:
                raise Exception("No response generated from Gemini")
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}", exc_info=True)
            
            # Try to list available models for debugging
            available_models_list = []
            try:
                if GEMINI_SDK_AVAILABLE:
                    available_models_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    logger.info(f"Available Gemini models: {available_models_list[:5]}...")  # Log first 5
            except Exception as list_error:
                logger.error(f"Could not list models: {list_error}")
            
            # Provide helpful error message
            error_msg = str(e)
            if "api key" in error_msg.lower() or "invalid" in error_msg.lower():
                error_msg = "API key issue - check GOOGLE_API_KEY in .env file"
            elif available_models_list:
                error_msg = f"Model error. Available models: {', '.join(available_models_list[:3])}"
            
            return {
                "response": f"Hey, I got your message but ran into an issue: {error_msg}. Mind checking the backend logs?",
                "model": requested_model if 'requested_model' in locals() else "error",
                "language": language or "en"
            }


# Global client instance
openai_client = OpenAIClient()
