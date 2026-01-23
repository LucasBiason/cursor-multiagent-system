"""
User Router

API endpoints for the users domain.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_db
from src.users import schemas, service
from src.users.exceptions import UserNotFoundError, UserAlreadyExistsError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    - **email**: User email (must be unique)
    - **name**: User name
    """
    try:
        return service.create_user(db, user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    Get user by ID.

    - **user_id**: User UUID
    """
    try:
        return service.get_user(db, user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/", response_model=schemas.UserListResponse)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List users with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records (default: 100, max: 1000)
    """
    if limit > 1000:
        limit = 1000
    
    users = service.list_users(db, skip=skip, limit=limit)
    total = len(users)  # In production, use count query
    
    return schemas.UserListResponse(
        items=users,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        page_size=limit,
    )


@router.patch("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: str,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update user.

    - **user_id**: User UUID
    - **email**: New email (optional)
    - **name**: New name (optional)
    - **is_active**: Active status (optional)
    """
    try:
        return service.update_user(db, user_id, user_data)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete user (soft delete).

    - **user_id**: User UUID
    """
    try:
        service.delete_user(db, user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

