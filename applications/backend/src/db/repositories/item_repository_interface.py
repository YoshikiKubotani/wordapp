from abc import ABC, abstractmethod

from src.domain.models import Item

from .base_repository_interface import IBaseRepository


class IItemRepository(IBaseRepository[Item], ABC):
    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[Item]:
        pass
