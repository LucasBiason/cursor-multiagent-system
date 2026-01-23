"""
User Domain Exceptions

Domain-specific exceptions for the users domain.
"""
from src.core.exceptions import AppException
from fastapi import status


class UserNotFoundError(AppException):
    """Raised when user is not found."""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UserAlreadyExistsError(AppException):
    """Raised when user already exists."""
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)

