from abc import ABC, abstractmethod

from src.domain.models import Quiz

from .base_repository_interface import IBaseRepository


class IQuizRepository(IBaseRepository[Quiz], ABC):
    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[Quiz]:
        pass

    @abstractmethod
    async def read_by_deck_id(self, deck_id: int) -> list[Quiz]:
        pass
