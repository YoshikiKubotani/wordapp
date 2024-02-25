from typing import Any

from fastapi import APIRouter, Depends

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
    """Get all users.

    Args:
        async_session (AsyncSession): The async session.

    Returns:
        list[UserResponse]: The list of all users.
    """
    users = [
        UserResponse(
            user_id=1,
            user_name="dummy_user_name",
            email="dummy_user",
            full_name="dummy_full_name",
        )
    ]
    return users


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserResponse,
)
async def create_user(
    user: CreateUserRequest,
    async_session: async_session_dependency,
) -> Any:
    """Create a new user.

    Args:
        user (CreateUserRequest): The user to create.
        async_session (AsyncSession): The async session.

    Returns:
        UserResponse: The created user.
    """
    return UserResponse(
        user_id=1,
        user_name="dummy_user_name",
        email="dummy_user",
        full_name="dummy_full_name",
    )


@router.get("/{user_name}", response_model=UserResponse)
async def read_own_user(
    user_name: str,
    currenct_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Get the details of a user.

    Args:
        user_name (str): The user name.
        currenct_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        UserResponse: The user details.
    """
    return currenct_user


@router.put("/{user_name}", response_model=UserResponse)
async def update_own_user(
    user_name: str,
    user: UpdateUserRequest,
    async_session: async_session_dependency,
) -> Any:
    """Update the details of a user.

    Args:
        user_name (str): The user name.
        user (UpdateUserRequest): The user details to update.
        async_session (AsyncSession): The async session.

    Returns:
        UserResponse: The updated user details.
    """
    return UserResponse(
        user_id=1,
        user_name="dummy_user_name",
        email="dummy_user",
        full_name="dummy_full_name",
    )


@router.delete("/{user_name}")
async def delete_own_user(
    user_name: str,
    async_session: async_session_dependency,
) -> bool:
    """Delete a user.

    Args:
        user_name (str): The user name.
        async_session (AsyncSession): The async session.

    Returns:
        bool: True if the user was deleted successfully.
    """
    return True
