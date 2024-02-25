from abc import ABC, abstractmethod

from src.domain.models import User, UserLoginHistory

from .base_repository_interface import IBaseRepository


class IUserRepository(IBaseRepository[User], ABC):
    @abstractmethod
    async def read_by_username(self, user_name: str) -> User | None:
        pass

    @abstractmethod
    async def read_by_email(self, email: str) -> User | None:
        pass


class IUserLoginHistoryRepository(IBaseRepository[UserLoginHistory], ABC):
    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[UserLoginHistory]:
        pass