"""
Pydantic schemas for memory save requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class MemorySaveRequest(BaseModel):
    """Request schema for saving a conversation memory"""
    user_id: int = Field(..., description="User ID")
    assistant_id: str = Field(..., description="Vapi Assistant ID")
    transcript: str = Field(..., description="Full conversation transcript")


class MemoryResponse(BaseModel):
    """Response schema for a single memory"""
    id: int = Field(..., description="Memory ID")
    user_id: int = Field(..., description="User ID")
    assistant_id: str = Field(..., description="Vapi Assistant ID")
    transcript: str = Field(..., description="Full conversation transcript")
    summary: str = Field(..., description="AI-generated summary")
    created_at: str = Field(..., description="ISO format timestamp")
    
    class Config:
        from_attributes = True


class MemorySaveResponse(BaseModel):
    """Response schema for memory save operation"""
    status: str = Field(..., description="Status of the save operation")
    memory_id: int = Field(..., description="ID of the saved memory")
    summary: str = Field(..., description="Generated summary")


class MemoryListResponse(BaseModel):
    """Response schema for list of memories"""
    memories: List[MemoryResponse] = Field(..., description="List of memories")
    count: int = Field(..., description="Number of memories returned")

