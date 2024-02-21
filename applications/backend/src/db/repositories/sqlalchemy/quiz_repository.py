from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyQuiz, orm_object_to_dict
from src.domain.models import Quiz

from .base_repository import BaseRepository


class QuizRepository(BaseRepository[SQLAlchemyQuiz, Quiz]):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(
            data_model=SQLAlchemyQuiz, domain_model=Quiz, async_seesoon=async_session
        )

    async def read_by_user_id(self, user_id: int) -> list[Quiz]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model).where(self.data_model.user_id == user_id).order_by(self.data_model.quiz_id)
            )
            quizzes = results.scalars().all()
        quizzes = [Quiz.model_validate(orm_object_to_dict(quiz)) for quiz in quizzes]
        return quizzes

    async def read_by_deck_id(self, deck_id: int) -> list[Quiz]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model).where(self.data_model.deck_id == deck_id).order_by(self.data_model.quiz_id)
            )
            quizzes = results.scalars().all()
        quizzes = [Quiz.model_validate(orm_object_to_dict(quiz)) for quiz in quizzes]
        return quizzes
