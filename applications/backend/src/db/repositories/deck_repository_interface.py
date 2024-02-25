from abc import ABC, abstractmethod

from src.domain.models import Deck

from .base_repository_interface import IBaseRepository


class IDeckRepository(IBaseRepository[Deck], ABC):
    """The interface for the deck repository."""

    @abstractmethod
    async def read_all(self) -> list[Deck]:
        """Read all decks from the database.

        Returns:
            list[Deck]: The list of all decks.
        """
        pass

    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[Deck]:
        """Read all decks from the database that belong to a specific user.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[Deck]: The list of decks that belong to the user.
        """
        pass
