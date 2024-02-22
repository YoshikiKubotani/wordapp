import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyDeck,
    SQLAlchemyQuiz,
    SQLAlchemyUser,
)
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import Deck, Quiz, User

pytestmark = pytest.mark.anyio

async def test_read_by_username(async_db_session: AsyncSession) -> None:
    """Test the `UserRepository.read_by_username` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create a user for testing.
    user_domain_model = User(
        user_id=1,
        user_name="dummy_user",
        email="dummy_email",
        password="dummy_password",
    )
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add(user_data_model)
        await async_db_session.flush()

    # Instantiate the `UserRepository` class.
    user_repository = UserRepository(async_db_session)
    # Get the user by username.
    user = await user_repository.read_by_username("dummy_user")
    # Test if the returned user is correct (i.e. equals to the one created above).
    assert user == user_domain_model