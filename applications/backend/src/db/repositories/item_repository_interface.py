from abc import ABC, abstractmethod

from src.domain.models import Item

from .base_repository_interface import IBaseRepository


class IItemRepository(IBaseRepository[Item], ABC):
    """The interface for the item repository."""

    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[Item]:
        """Read all items from the database that were made by a specific user.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[Item]: The list of items that were made by the user.
        """
        pass
