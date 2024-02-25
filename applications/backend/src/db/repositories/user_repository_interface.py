from abc import ABC, abstractmethod

from src.domain.models import User, UserLoginHistory

from .base_repository_interface import IBaseRepository


class IUserRepository(IBaseRepository[User], ABC):
    """The interface for the user repository."""

    @abstractmethod
    async def read_by_username(self, user_name: str) -> User | None:
        """Read a user from the database by their username.

        Args:
            user_name (str): The username of the user.

        Returns:
            User | None: The user with the username, or None if not found.
        """
        pass

    @abstractmethod
    async def read_by_email(self, email: str) -> User | None:
        """Read a user from the database by their email.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The user with the email, or None if not found.
        """
        pass


class IUserLoginHistoryRepository(IBaseRepository[UserLoginHistory], ABC):
    """The interface for the user login history repository."""

    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[UserLoginHistory]:
        """Read all login history from the database that belong to a specific user.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[UserLoginHistory]: The list of login history that belong to the user.
        """
        pass
