"""
API endpoints for saving and retrieving conversation memories
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Memory, User
from app.schemas.memory import (
    MemoryResponse,
    MemoryListResponse,
    MemorySaveRequest,
    MemorySaveResponse
)
from app.services.openai_client import openai_client

router = APIRouter()


@router.post("/save", response_model=MemorySaveResponse)
async def save_memory(
    request: MemorySaveRequest,
    db: Session = Depends(get_db)
):
    """
    Save a conversation transcript and generate a summary using Gemini AI.
    
    This endpoint:
    1. Receives transcript from frontend (after Vapi voice call ends)
    2. Generates a summary using Gemini Flash (free)
    3. Stores both transcript and summary in database
    
    Args:
        request: MemorySaveRequest with user_id, assistant_id, and transcript
        db: Database session
    
    Returns:
        MemorySaveResponse with status, memory_id, and generated summary
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {request.user_id} not found"
            )
        
        # Generate summary using Gemini AI
        summary_prompt = f"""Please provide a concise summary (2-3 sentences) of this conversation transcript:

{request.transcript}

Summary:"""
        
        summary_response = await openai_client.send_message(
            message=summary_prompt,
            model="gemini-1.5-flash"
        )
        
        summary = summary_response.get("response", "No summary generated")
        
        # Clean up summary if it contains extra text
        if "Summary:" in summary:
            summary = summary.split("Summary:")[-1].strip()
        if "summary:" in summary.lower():
            summary = summary.split("summary:")[-1].strip()
        
        # Create memory record
        memory = Memory(
            user_id=request.user_id,
            assistant_id=request.assistant_id,
            transcript=request.transcript,
            summary=summary
        )
        
        db.add(memory)
        db.commit()
        db.refresh(memory)
        
        return MemorySaveResponse(
            status="saved",
            memory_id=memory.id,
            summary=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save memory: {str(e)}"
        )


@router.get("/{user_id}", response_model=MemoryListResponse)
async def get_memories(
    user_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all memories for a specific user, ordered by most recent first.
    
    Args:
        user_id: ID of the user to fetch memories for
        limit: Maximum number of memories to return (default: 100)
        db: Database session
    
    Returns:
        List of memories with id, user_id, assistant_id, transcript, summary, and created_at
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User with id {user_id} not found"
            )
        
        memories = db.query(Memory)\
            .filter(Memory.user_id == user_id)\
            .order_by(desc(Memory.created_at))\
            .limit(limit)\
            .all()
        
        return MemoryListResponse(
            memories=[
                MemoryResponse(
                    id=memory.id,
                    user_id=memory.user_id,
                    assistant_id=memory.assistant_id,
                    transcript=memory.transcript,
                    summary=memory.summary,
                    created_at=memory.created_at.isoformat()
                )
                for memory in memories
            ],
            count=len(memories)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch memories: {str(e)}"
        )


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific memory by ID.
    
    Args:
        memory_id: ID of the memory to delete
        db: Database session
    
    Returns:
        Success message with deleted memory ID
    """
    try:
        memory = db.query(Memory).filter(Memory.id == memory_id).first()
        
        if not memory:
            raise HTTPException(
                status_code=404,
                detail=f"Memory with id {memory_id} not found"
            )
        
        db.delete(memory)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Memory {memory_id} deleted successfully",
            "deleted_id": memory_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete memory: {str(e)}"
        )
