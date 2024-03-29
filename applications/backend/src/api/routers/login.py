from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies import async_session_dependency
from src.api.schemas import Token
from src.core.config import settings
from src.core.security import (
    authenticate_user,
    create_access_token,
)

router = APIRouter()


@router.post("/login/access-token")
async def login(
    async_session: async_session_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Log in and get an access token.

    Args:
        async_session (AsyncSession): The async session.
        form_data (OAuth2PasswordRequestForm): The form data.

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        Token: The access token.
    """
    # Check if the user exists and the password is correct.
    user = await authenticate_user(
        async_session,
        form_data.username,
        form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create a new access token for the verified user.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.user_name, expires_delta=access_token_expires
    )
    print(
        f"Issued a verfied token for {user.user_name} which will expire in {access_token_expires}."
    )
    print(f"token: {access_token}")

    return Token(access_token=access_token, token_type="bearer")
