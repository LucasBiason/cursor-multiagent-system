"""
API v1 Router Registration

Register all domain routers here.
"""
from fastapi import APIRouter

# Import domain routers
from src.users.router import router as users_router

api_router = APIRouter()

# Register domain routers
api_router.include_router(users_router, tags=["users"])

