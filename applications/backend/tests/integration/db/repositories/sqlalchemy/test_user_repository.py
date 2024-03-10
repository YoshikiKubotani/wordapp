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
from tests.utils import DomainModelDict

pytestmark = pytest.mark.anyio


class TestUserRepositorySuccess:
    """Test cases for the `UserRepository` class when successful."""

    async def test_read_by_username(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `UserRepository.read_by_username` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `UserRepository` class.
        user_repository = UserRepository(async_db_session)
        # Get the user by username.
        user = await user_repository.read_by_username("dummy_user1")
        # Test if the returned user is correct (i.e. equals to the one created above).
        assert user == domain_model_dict["user_domain_models"][0]

    async def test_read_by_email(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `UserRepository.read_by_email` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `UserRepository` class.
        user_repository = UserRepository(async_db_session)
        # Get the user by email.
        user = await user_repository.read_by_email("dummy_email1")
        # Test if the returned user is correct (i.e. equals to the one created above).
        assert user == domain_model_dict["user_domain_models"][0]


class TestUserLoginHistoryRepositorySuccess:
    """Test cases for the `UserLoginHistoryRepository` class when successful."""

    async def test_user_login_read_by_user_id(
        self, repository_class_provision: tuple[AsyncSession, DomainModelDict]
    ) -> None:
        """Test the `UserLoginHistoryRepository.read_by_user_id` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `UserRepository` class.
        user_login_history_repository = UserLoginHistoryRepository(async_db_session)
        # Get the user login history by user_id.
        user1_login_history = await user_login_history_repository.read_by_user_id(
            user_id=1
        )
        user2_login_history = await user_login_history_repository.read_by_user_id(
            user_id=2
        )
        # Test if the returned user login history is correct (i.e. equals to the one created above).
        assert len(user1_login_history) == 2
        assert user1_login_history[0] == domain_model_dict["user_login_history_domain_models"][0]
        assert user1_login_history[1] == domain_model_dict["user_login_history_domain_models"][1]
        assert len(user2_login_history) == 1
        assert user2_login_history[0] == domain_model_dict["user_login_history_domain_models"][2]
