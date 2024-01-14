from typing import Any

from fastapi import APIRouter, HTTPException, Depends

from new_src.api.dependencies import (
    CurrentUser,
    # SessionDep,
    get_current_active_superuser,
)
from new_src.api.schemas import CreateUserRequest, UpdateUserRequest, UserResponse

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[UserResponse],
)
def read_all_users(
    # session: SessionDep = Depends(get_session),
) -> Any:
    """Get all users."""
    users = [UserResponse(user_id=1, email="dummy_user")]
    return users


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserResponse,
)
def create_user(
    # user: CreateUserRequest,
    # session: SessionDep = Depends(get_session),
) -> Any:
    """Create a new user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.get("/{user_name}", response_model=UserResponse)
def read_own_user(
    # user_name: str,
    # session: SessionDep = Depends(get_session),
) -> Any:
    """Get the details of a user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.put("/{user_name}", response_model=UserResponse)
def update_own_user(
    # user_name: str,
    # user: UpdateUserRequest,
    # session: SessionDep = Depends(get_session),
) -> Any:
    """Update the details of a user."""
    return UserResponse(user_id=1, email="dummy_user")


@router.delete("/{user_name}")
def delete_own_user(
    # user_name: str,
    # session: SessionDep = Depends(get_session),
) -> bool:
    """Delete a user."""
    return True
