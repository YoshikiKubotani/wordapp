from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    orm_object_to_dict,
)
from src.db.repositories.user_repository_interface import (
    IUserLoginHistoryRepository,
    IUserRepository,
)
from src.domain.models import User, UserLoginHistory

from .base_repository import BaseRepository


class UserRepository(BaseRepository[SQLAlchemyUser, User], IUserRepository):
    """The SQLAlchemy repository class for users."""

    def __init__(self, async_session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            async_session (AsyncSession): The asynchronous session to use for database operations.
        """
        super().__init__(
            data_model=SQLAlchemyUser, domain_model=User, async_seesoon=async_session
        )

    async def read_by_username(self, user_name: str) -> User | None:
        """Read a user from the database by their username.

        Args:
            user_name (str): The username of the user.

        Returns:
            User | None: The user with the username, or None if not found.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.user_name == user_name)
                .order_by(self.data_model.user_id)
            )
            user = results.scalars().one_or_none()
        if user is None:
            return user
        else:
            user = User.model_validate(orm_object_to_dict(user))
            return cast(User, user)

    async def read_by_email(self, email: str) -> User | None:
        """Read a user from the database by their email.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The user with the email, or None if not found.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.email == email)
                .order_by(self.data_model.user_id)
            )
            user = results.scalars().one_or_none()
        if user is None:
            return user
        else:
            user = User.model_validate(orm_object_to_dict(user))
            return cast(User, user)


class UserLoginHistoryRepository(
    BaseRepository[SQLAlchemyUserLoginHistory, UserLoginHistory],
    IUserLoginHistoryRepository,
):
    """The SQLAlchemy repository class for user login histories."""

    def __init__(self, async_session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            async_session (AsyncSession): The asynchronous session to use for database operations.
        """
        super().__init__(
            data_model=SQLAlchemyUserLoginHistory,
            domain_model=UserLoginHistory,
            async_seesoon=async_session,
        )

    async def read_by_user_id(self, user_id: int) -> list[UserLoginHistory]:
        """Read all user login histories from the database that belong to a specific user.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[UserLoginHistory]: The list of user login histories that belong to the user.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.user_id == user_id)
                .order_by(self.data_model.user_login_history_id)
            )
            user_login_histories = results.scalars().all()
        user_login_histories = [
            UserLoginHistory.model_validate(orm_object_to_dict(user_login_history))
            for user_login_history in user_login_histories
        ]
        return user_login_histories
