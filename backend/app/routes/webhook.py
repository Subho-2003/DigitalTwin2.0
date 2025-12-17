"""
Vapi webhook endpoint for receiving structured outputs
Note: This is optional - frontend saves memories directly via /api/memory/save
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging

from app.database import get_db
from app.models import Memory, User

router = APIRouter()
logger = logging.getLogger(__name__)


def is_meaningful_content(content: str) -> bool:
    """
    Check if content is meaningful (not empty or just whitespace).
    Filters out empty strings and very short meaningless content.
    """
    if not content:
        return False
    content = content.strip()
    # Ignore empty strings or very short content (less than 10 chars)
    if len(content) < 10:
        return False
    return True


@router.post("/vapi/webhook")
async def vapi_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Vapi webhook events.
    
    Note: This webhook is optional. The frontend handles saving memories
    directly via POST /api/memory/save after voice calls end.
    
    If you want to use webhooks, you'll need to:
    1. Configure webhook URL in Vapi dashboard
    2. Ensure webhook payload includes user_id and assistant_id
    3. Or use a default user_id if not provided
    
    Expected webhook payload structure:
    {
        "call": {
            "assistantId": "...",
            "customer": {"number": "..."},
            "analysis": {
                "structuredOutputs": {
                    "callSummary": "...",
                    "memoryCandidate": "..."
                }
            },
            "transcript": "..."
        }
    }
    """
    try:
        # Get webhook payload
        payload: Dict[str, Any] = await request.json()
        logger.info(f"Received Vapi webhook: {payload.get('type', 'unknown')}")
        
        # Safely extract data
        call_data = payload.get("call", {})
        analysis = call_data.get("analysis", {})
        structured_outputs = analysis.get("structuredOutputs", {})
        
        # Extract assistant ID and transcript
        assistant_id = call_data.get("assistantId", "")
        transcript = call_data.get("transcript", "")
        
        # Get or use default user_id (webhook might not have user info)
        # For webhooks, we'll use a default user or create one
        default_user = db.query(User).filter(User.email == "webhook@system").first()
        if not default_user:
            # Create a default user for webhook saves
            default_user = User(name="Webhook User", email="webhook@system")
            db.add(default_user)
            db.commit()
            db.refresh(default_user)
            logger.info(f"Created default webhook user: {default_user.id}")
        
        user_id = default_user.id
        
        saved_items = []
        
        # Extract call summary - save as memory with summary
        call_summary = structured_outputs.get("callSummary")
        if call_summary and is_meaningful_content(call_summary):
            if transcript or call_summary:
                try:
                    # Save as memory with summary
                    memory_record = Memory(
                        user_id=user_id,
                        assistant_id=assistant_id or "unknown",
                        transcript=transcript or call_summary,  # Use transcript if available, else summary
                        summary=call_summary.strip()
                    )
                    db.add(memory_record)
                    db.commit()
                    db.refresh(memory_record)
                    saved_items.append(f"Memory with summary (id: {memory_record.id})")
                    logger.info(f"Saved memory from webhook: {memory_record.id}")
                except Exception as e:
                    logger.error(f"Error saving memory from webhook: {e}")
                    db.rollback()
        
        # Extract memory candidate - can be saved separately or merged
        memory_candidate = structured_outputs.get("memoryCandidate")
        if memory_candidate and is_meaningful_content(memory_candidate):
            # If we already saved a summary, append candidate to it
            # Otherwise, save as new memory
            if saved_items:
                # Update the last saved memory to include candidate info
                try:
                    last_memory = db.query(Memory).filter(
                        Memory.user_id == user_id,
                        Memory.assistant_id == assistant_id or "unknown"
                    ).order_by(Memory.id.desc()).first()
                    if last_memory:
                        last_memory.summary += f"\n\nMemory: {memory_candidate.strip()}"
                        db.commit()
                        saved_items.append(f"Updated memory {last_memory.id} with candidate")
                except Exception as e:
                    logger.error(f"Error updating memory: {e}")
            else:
                # Save as new memory
                try:
                    memory_record = Memory(
                        user_id=user_id,
                        assistant_id=assistant_id or "unknown",
                        transcript=transcript or memory_candidate,
                        summary=memory_candidate.strip()
                    )
                    db.add(memory_record)
                    db.commit()
                    db.refresh(memory_record)
                    saved_items.append(f"Memory candidate (id: {memory_record.id})")
                    logger.info(f"Saved memory candidate: {memory_record.id}")
                except Exception as e:
                    logger.error(f"Error saving memory candidate: {e}")
                    db.rollback()
        
        # Return success response
        return {
            "status": "success",
            "message": "Webhook processed",
            "saved": saved_items if saved_items else "No data to save (webhook payload might need user_id)"
        }
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        # Return 200 to prevent Vapi from retrying
        return {
            "status": "error",
            "message": f"Error processing webhook: {str(e)}"
        }

