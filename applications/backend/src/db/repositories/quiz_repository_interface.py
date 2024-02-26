from abc import ABC, abstractmethod

from src.domain.models import Quiz

from .base_repository_interface import IBaseRepository


class IQuizRepository(IBaseRepository[Quiz], ABC):
    """The interface for the quiz repository."""

    @abstractmethod
    async def read_by_user_id(self, user_id: int) -> list[Quiz]:
        """Read all quizzes from the database that a specific user has taken.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[Quiz]: The list of quizzes that the user has taken.
        """
        pass

    @abstractmethod
    async def read_by_deck_id(self, deck_id: int) -> list[Quiz]:
        """Read all quizzes from the database that were based on a specific deck.

        Args:
            deck_id (int): The unique identifier for the deck.

        Returns:
            list[Quiz]: The list of quizzes that were based on the deck.
        """
        pass
