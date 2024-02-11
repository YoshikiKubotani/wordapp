import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
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
    user_repository = UserRepository()

    # Check if the user already exists.
    user = await user_repository.read_by_email(email=email)
    # Create a random user if it doesn't exist.
    if user is None:
        # Generate a random password.
        password = random_lower_string()
        user_in = User(
            user_name=email,
            email=email,
            password=password,
        )
        user = await user_repository.create(async_session, user_in)
    return user