import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import AliasChoices, BaseModel, Field
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.db.models.sqlalchemy_data_models import SQLAlchemyUser
from src.db.repositories.sqlalchemy.base_repository import BaseRepository
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import Deck, Quiz, User, UserLoginHistory

pytestmark = pytest.mark.anyio

async def test_create(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.create` method.

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

    # Instantiate the `BaseRepository` class.
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    # Create a user.
    user = await user_repository.create(user_domain_model)
    # Test if the returned user is correct (i.e. equals to the one created above).
    assert user == user_domain_model

async def test_read(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.read` method.

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
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    # Get the user by ID.
    user = await user_repository.read(id=1)
    # Test if the returned user is correct (i.e. equals to the one created above).
    assert user == user_domain_model

async def test_update(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.update` method.

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
    updated_user_domain_model = User(
        user_id=1,
        user_name="updated_dummy_user",
        email="updated_dummy_email",
        password="updated_dummy_password",
    )
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add(user_data_model)
        await async_db_session.flush()

    # Instantiate the `UserRepository` class.
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    # Update the user.
    user = await user_repository.update(updated_user_domain_model)
    # Test if the returned user is correct (i.e. equals to the one created above).
    assert user == updated_user_domain_model

async def test_delete(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.delete` method.

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
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    # Delete the user.
    await user_repository.delete(id=1)
    # Test if the user is deleted.
    with pytest.raises(ValueError):
        await user_repository.read(id=1)