from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from src.api.dependencies import async_session_dependency
from src.core.config import settings
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


async def authenticate_user(
    async_session: async_session_dependency,
    user_name: str,
    password: str,
) -> User | None:
    user_repository = UserRepository(async_session)

    # Check if the incoming user exists.
    user = await user_repository.read_by_username(user_name)

    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
