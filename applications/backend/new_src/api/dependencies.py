from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from new_src.core.config import settings
from new_src.api.schemas import TokenPayload, User, DummyUser

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/access-token"
)

# def get_db() -> Generator:
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(
        # session: SessionDep,
        token: TokenDep
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
        hashed_password="$2b$12$Z3wv6Y5wqQ9RZ7x7tXv6IeQ2jzR0YVW8Q8b6N4Yf6RZ5n0V7YJZ4S"
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
        )
    return current_user