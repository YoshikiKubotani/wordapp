import random
import string

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.security import get_password_hash
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def create_random_test_user(async_session: AsyncSession, email: str) -> User:
    """Create a random normal user in the database for testing.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.
        email (str): The dummy email of the test user.

    Returns:
        User: The user that was created.
    """
    user_repository = UserRepository(async_session)

    # Check if the user already exists.
    user = await user_repository.read_by_email(email)
    # Create a random user if it doesn't exist.
    if user is None:
        print("Creating a normal user for testing.")
        # Generate a random password.
        password = random_lower_string()
        user_in = User(
            user_name=email,
            email=email,
            password=get_password_hash(password),
        )
        user = await user_repository.create(user_in)

        # For system-related reasons, it is necessary to revert the password back to its original, unhashed value.
        user.password = password
    return user


async def create_test_superuser(async_session: AsyncSession) -> User:
    """Create a superuser in the database for testing.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.

    Returns:
        User: The superuser that was created.
    """
    user_repository = UserRepository(async_session)

    # Check if the user already exists.
    user = await user_repository.read_by_email(settings.FIRST_SUPERUSER_EMAIL)
    # Create a superuser if it doesn't exist.
    if user is None:
        print("Creating a superuser for testing.")
        user_in = User(
            user_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        user = await user_repository.create(user_in)

        # For system-related reasons, it is necessary to revert the password back to its original, unhashed value.
        user.password = settings.FIRST_SUPERUSER_PASSWORD
    return user
