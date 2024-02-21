from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyQuizItem, orm_object_to_dict
from src.domain.models import QuizItem

from .base_repository import BaseRepository


class QuizItemRepository(BaseRepository[SQLAlchemyQuizItem, QuizItem]):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(
            data_model=SQLAlchemyQuizItem,
            domain_model=QuizItem,
            async_seesoon=async_session,
        )

    async def read_by_quiz_id(self, quiz_id: int) -> list[QuizItem]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model).where(self.data_model.quiz_id == quiz_id).order_by(self.data_model.quiz_item_id)
            )
            quiz_items = results.scalars().all()
        quiz_items = [QuizItem.model_validate(orm_object_to_dict(quiz_item)) for quiz_item in quiz_items]
        return quiz_items

    async def read_by_item_id(self, item_id: int) -> list[QuizItem]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            quiz_items = await self.async_session.execute(
                select(self.data_model).where(self.data_model.item_id == item_id).order_by(self.data_model.quiz_item_id)
            )
            quiz_items = quiz_items.scalars().all()
        quiz_items = [QuizItem.model_validate(orm_object_to_dict(quiz_item)) for quiz_item in quiz_items]
        return quiz_items
