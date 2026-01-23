"""
User Service

Business logic for the users domain.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.users import models, schemas
from src.users.exceptions import UserNotFoundError, UserAlreadyExistsError


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    """
    Create a new user.

    Args:
        db: Database session
        user_data: User creation data

    Returns:
        Created user

    Raises:
        UserAlreadyExistsError: If user with email already exists
    """
    try:
        user = models.User(
            email=user_data.email,
            name=user_data.name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError(f"User with email {user_data.email} already exists")


def get_user(db: Session, user_id: str) -> models.User:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User

    Raises:
        UserNotFoundError: If user not found
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"User with id {user_id} not found")
    return user


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Get user by email.

    Args:
        db: Database session
        email: User email

    Returns:
        User or None if not found
    """
    return db.query(models.User).filter(models.User.email == email).first()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    """
    List users with pagination.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of users
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, user_data: schemas.UserUpdate) -> models.User:
    """
    Update user.

    Args:
        db: Database session
        user_id: User ID
        user_data: User update data

    Returns:
        Updated user

    Raises:
        UserNotFoundError: If user not found
    """
    user = get_user(db, user_id)
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> None:
    """
    Delete user (soft delete by setting is_active=False).

    Args:
        db: Database session
        user_id: User ID

    Raises:
        UserNotFoundError: If user not found
    """
    user = get_user(db, user_id)
    user.is_active = False
    db.commit()

