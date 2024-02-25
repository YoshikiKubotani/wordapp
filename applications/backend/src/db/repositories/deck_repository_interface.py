from abc import ABC, abstractmethod

from src.domain.models import Deck

from .base_repository_interface import IBaseRepository


class IDeckRepository(IBaseRepository[Deck], ABC):
    @abstractmethod
    async def read_all(self) -> list[Deck]:
        pass

    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[Deck]:
        pass
