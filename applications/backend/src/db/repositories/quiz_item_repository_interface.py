from abc import ABC, abstractmethod

from src.domain.models import QuizItem

from .base_repository_interface import IBaseRepository


class IQuizItemRepository(IBaseRepository[QuizItem], ABC):
    """The interface for the quiz item repository."""

    @abstractmethod
    async def read_by_quiz_id(self, quiz_id: int) -> list[QuizItem]:
        """Read all quiz items from the database that belong to a specific quiz.

        Args:
            quiz_id (int): The unique identifier for the quiz.

        Returns:
            list[QuizItem]: The list of quiz items that belong to the quiz.
        """
        pass

    @abstractmethod
    async def read_by_item_id(self, item_id: int) -> list[QuizItem]:
        """Read all quiz items from the database that ask for a specific item.

        Args:
            item_id (int): The unique identifier for the item.

        Returns:
            list[QuizItem]: The list of quiz items that ask for the item.
        """
        pass
