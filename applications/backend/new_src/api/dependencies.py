from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from new_src.api.schemas import DummyUser, TokenPayload, User
from new_src.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from new_src.core.main import AsyncSessionFactory
    async with AsyncSessionFactory() as session:
        yield session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(
    async_session: AsyncSessionDep,
    token: TokenDep,
) -> User:
    try:
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
    user = DummyUser(
        user_name=token_data.sub,
        email="dummy@gmail.com",
        full_name="dummy user",
        is_active=True,
        is_superuser=True,
        hashed_password="$2b$12$gjLw4vccsNb41k/eHJeGtemKhjzw3aKxW6ANle2ZXzJTfhiRyvgNy",
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_superuser(current_user: CurrentUserDep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user
