from abc import ABC, abstractmethod

from src.domain.models import QuizItem

from .base_repository_interface import IBaseRepository


class IQuizItemRepository(IBaseRepository[QuizItem], ABC):
    @abstractmethod
    async def read_by_quiz_id(self, quiz_id: int) -> list[QuizItem]:
        pass

    @abstractmethod
    async def read_by_item_id(self, item_id: int) -> list[QuizItem]:
        pass