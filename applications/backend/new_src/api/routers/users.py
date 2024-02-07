from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from new_src.api.dependencies import (
    AsyncSessionDep,
    CurrentUserDep,
    get_current_active_superuser,
)
from new_src.api.schemas import CreateUserRequest, UpdateUserRequest, UserResponse

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[UserResponse],
)
async def read_all_users(
    async_session: AsyncSessionDep,
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
    async_session: AsyncSessionDep,
) -> Any:
    """Create a new user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.get("/{user_name}", response_model=UserResponse)
async def read_own_user(
    # user_name: str,
    currenct_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Get the details of a user."""
    return currenct_user


@router.put("/{user_name}", response_model=UserResponse)
async def update_own_user(
    # user_name: str,
    # user: UpdateUserRequest,
    async_session: AsyncSessionDep,
) -> Any:
    """Update the details of a user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.delete("/{user_name}")
async def delete_own_user(
    # user_name: str,
    async_session: AsyncSessionDep,
) -> bool:
    """Delete a user."""
    return True
