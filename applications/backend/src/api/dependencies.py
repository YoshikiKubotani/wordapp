from datetime import datetime, timezone
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import TokenPayload
from src.core.config import settings
from src.domain.models import User

# Create a callable object that will look for and parse the request for the `Authorization` header
# Note that the `tokenUrl` parameter is only used for the OpenAPI documentation, not for the authentication itself
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from src.core.main import AsyncSessionFactory

    # This context automatically calls async_session.close() when the code block is exited.
    async with AsyncSessionFactory() as async_session:
        yield async_session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
    async_session: AsyncSessionDep,
    token: TokenDep,
) -> User:
    try:
        print(f"Received a request with authentication header of token {token}.")
        # Decode the received token and extract the payload.  Note that the payload will not be
        # correctly retrieved unless the jwt is encrypted with the secret key and algorithm
        # used during authentication (login)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # user = session.get(User, token_data.sub)
    user = User(
        user_id=1,
        user_name=token_data.sub,
        email="dummy@gmail.com",
        password="$2b$12$gjLw4vccsNb41k/eHJeGtemKhjzw3aKxW6ANle2ZXzJTfhiRyvgNy",
        full_name="dummy user",
        is_active=True,
        is_superuser=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUserDep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user
