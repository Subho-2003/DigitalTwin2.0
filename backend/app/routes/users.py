"""
User management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models import User

router = APIRouter()


class UserCreateRequest(BaseModel):
    """Request schema for creating a user"""
    name: str
    email: str  # Email validation can be added later if needed


class UserResponse(BaseModel):
    """Response schema for a user"""
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


@router.post("/create", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    
    For demo purposes - in production, this should be part of your auth system.
    
    Args:
        request: UserCreateRequest with name and email
        db: Database session
    
    Returns:
        UserResponse with created user details
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f"User with email {request.email} already exists"
            )
        
        # Create new user
        user = User(
            name=request.name,
            email=request.email
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user by ID.
    
    Args:
        user_id: ID of the user
        db: Database session
    
    Returns:
        UserResponse with user details
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )

