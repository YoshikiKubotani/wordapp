from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import (
    async_session_dependency,
    current_user_dependency,
    get_current_active_superuser,
)
from src.api.schemas import CreateUserRequest, UpdateUserRequest, UserResponse

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[UserResponse],
)
async def read_all_users(
    async_session: async_session_dependency,
) -> Any:
    """Get all users."""
    users = [UserResponse(user_id=1, email="dummy_user")]
    return users


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserResponse,
)
async def create_user(
    # user: CreateUserRequest,
    async_session: async_session_dependency,
) -> Any:
    """Create a new user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.get("/{user_name}", response_model=UserResponse)
async def read_own_user(
    # user_name: str,
    currenct_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Get the details of a user."""
    return currenct_user


@router.put("/{user_name}", response_model=UserResponse)
async def update_own_user(
    # user_name: str,
    # user: UpdateUserRequest,
    async_session: async_session_dependency,
) -> Any:
    """Update the details of a user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.delete("/{user_name}")
async def delete_own_user(
    # user_name: str,
    async_session: async_session_dependency,
) -> bool:
    """Delete a user."""
    return True
