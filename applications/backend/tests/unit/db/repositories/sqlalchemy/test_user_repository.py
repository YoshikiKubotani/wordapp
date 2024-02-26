import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
)
from src.db.repositories.sqlalchemy.user_repository import (
    UserLoginHistoryRepository,
    UserRepository,
)
from src.domain.models import User, UserLoginHistory

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

    # Instantiate the `UserRepository` class.
    user_repository = UserRepository(async_db_session)
    # Get the user by username.
    user = await user_repository.read_by_username("dummy_user")
    # Test if the returned user is correct (i.e. equals to the one created above).
    assert user == user_domain_model


async def test_read_by_email(async_db_session: AsyncSession) -> None:
    """Test the `UserRepository.read_by_email` method.

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

    # Instantiate the `UserRepository` class.
    user_repository = UserRepository(async_db_session)
    # Get the user by email.
    user = await user_repository.read_by_email("dummy_email")
    # Test if the returned user is correct (i.e. equals to the one created above).
    assert user == user_domain_model


async def test_user_login_read_by_user_id(async_db_session: AsyncSession) -> None:
    """Test the `UserLoginHistoryRepository.read_by_user_id` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create two users and three user login histories for testing.
    user1_domain_model = User(
        user_id=1,
        user_name="dummy_user1",
        email="dummy_email1",
        password="dummy_password1",
    )
    user2_domain_model = User(
        user_id=2,
        user_name="dummy_user2",
        email="dummy_email2",
        password="dummy_password2",
    )
    user_login_history1_domain_model = UserLoginHistory(
        user_login_history_id=1,
        user_id=1,
        ip_address="127.0.0.1",
    )
    user_login_history2_domain_model = UserLoginHistory(
        user_login_history_id=2,
        user_id=1,
        ip_address="127.0.0.1",
    )
    user_login_history3_domain_model = UserLoginHistory(
        user_login_history_id=3,
        user_id=2,
        ip_address="127.0.0.2",
    )
    user1_data_model = SQLAlchemyUser(**user1_domain_model.model_dump())
    user2_data_model = SQLAlchemyUser(**user2_domain_model.model_dump())
    user_login_history1_data_model = SQLAlchemyUserLoginHistory(
        **user_login_history1_domain_model.model_dump()
    )
    user_login_history2_data_model = SQLAlchemyUserLoginHistory(
        **user_login_history2_domain_model.model_dump()
    )
    user_login_history3_data_model = SQLAlchemyUserLoginHistory(
        **user_login_history3_domain_model.model_dump()
    )
    async with async_db_session.begin():
        async_db_session.add_all(
            [
                user1_data_model,
                user2_data_model,
                user_login_history1_data_model,
                user_login_history2_data_model,
                user_login_history3_data_model,
            ]
        )

    # Instantiate the `UserRepository` class.
    user_login_history_repository = UserLoginHistoryRepository(async_db_session)
    # Get the user login history by user_id.
    user1_login_history = await user_login_history_repository.read_by_user_id(user_id=1)
    user2_login_history = await user_login_history_repository.read_by_user_id(user_id=2)
    # Test if the returned user login history is correct (i.e. equals to the one created above).
    assert len(user1_login_history) == 2
    assert user1_login_history[0] == user_login_history1_domain_model
    assert user1_login_history[1] == user_login_history2_domain_model
    assert len(user2_login_history) == 1
    assert user2_login_history[0] == user_login_history3_domain_model
