from datetime import datetime, timedelta, timezone
from typing import cast

from jose import jwt
from passlib.context import CryptContext

from src.api.dependencies import async_session_dependency
from src.core.config import settings
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the plain password matches the hashed password when hashed, False otherwise.
    """
    return cast(bool, password_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Get the password hash.

    Args:
        password (str): The plain password.

    Returns:
        str: The hashed password.
    """
    return cast(str, password_context.hash(password))


async def authenticate_user(
    async_session: async_session_dependency,
    user_name: str,
    password: str,
) -> User | None:
    """Authenticate the user by verifying the given username and password against the registration information.

    Args:
        async_session (AsyncSession): The async session dependency.
        user_name (str): The username.
        password (str): The password.

    Returns:
        User | None: The user if the username and password are correct, None otherwise.
    """
    user_repository = UserRepository(async_session)

    # Check if the incoming user exists.
    user = await user_repository.read_by_username(user_name)

    # If the user does not exist, return None.
    if user is None:
        return None
    # If the password is incorrect, return None.
    if not verify_password(password, user.password):
        return None
    # If the user exists and the password is correct, return the user.
    return user


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Create an authentication token in the JSON Web Signature(JWS) format.

    Args:
        subject (str): The subject of the token.
        expires_delta (timedelta | None): The expiration time of the token.

    Returns:
        str: The encoded
    """
    # If the expiration time is given, set the expiration time to the given time.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    # If the expiration time is not given, set the expiration time to the default time.
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    # Define the payload of the JWS data.
    payload = {"sub": subject, "exp": expire}
    # Creates JWS data with the payload (and headers) encrypted with the specified algorithm.
    # `settings.SECRET_KEY` is used as the encryption key.
    access_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return cast(str, access_token)
