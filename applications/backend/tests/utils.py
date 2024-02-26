import random
import string

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.security import get_password_hash
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User


def random_lower_string() -> str:
    """Generate a random string of lowercase letters.

    Returns:
        str: The random string.
    """
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Generate a random email address.

    Returns:
        str: The random email address.
    """
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def create_random_test_user(async_session: AsyncSession) -> dict[str, str]:
    """Create a random normal user in the database for testing.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.

    Returns:
        dict[str, str]: The request form to log in as the created user.
    """
    user_repository = UserRepository(async_session)

    # Generate a random password.
    password = random_lower_string()

    # Check if the user already exists.
    user = await user_repository.read_by_email(settings.TEST_USER_EMAIL)
    # Create a random user if it doesn't exist.
    user_in = User(
        user_name=settings.TEST_USER_EMAIL,
        email=settings.TEST_USER_EMAIL,
        password=get_password_hash(password),
    )
    if user is None:
        print("Creating a normal user for testing.")
        user = await user_repository.create(user_in)
    else:
        print("Updating the password of the existing user for testing.")
        user = await user_repository.update(user_in)

    return {
        "username": settings.TEST_USER_EMAIL,
        "password": password,
    }


async def create_test_superuser(async_session: AsyncSession) -> dict[str, str]:
    """Create a superuser in the database for testing.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.

    Returns:
        dict[str, str]: The request form to log in as the created superuser.
    """
    user_repository = UserRepository(async_session)

    # Check if the user already exists.
    user = await user_repository.read_by_email(settings.FIRST_SUPERUSER_EMAIL)
    # Create a superuser if it doesn't exist.
    user_in = User(
        user_name=settings.FIRST_SUPERUSER,
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        is_superuser=True,
    )
    if user is None:
        print("Creating a superuser for testing.")
        user = await user_repository.create(user_in)
    else:
        print("Updating the password of the existing superuser for testing.")
        user = await user_repository.update(user_in)

    return {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
