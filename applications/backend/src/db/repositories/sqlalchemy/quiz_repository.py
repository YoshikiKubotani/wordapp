from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyQuiz, orm_object_to_dict
from src.db.repositories.quiz_repository_interface import IQuizRepository
from src.domain.models import Quiz

from .base_repository import BaseRepository


class QuizRepository(BaseRepository[SQLAlchemyQuiz, Quiz], IQuizRepository):
    """The SQLAlchemy repository class for quizzes."""

    def __init__(self, async_session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            async_session (AsyncSession): The asynchronous session to use for database operations.
        """
        super().__init__(
            data_model=SQLAlchemyQuiz, domain_model=Quiz, async_seesoon=async_session
        )

    async def read_by_user_id(self, user_id: int) -> list[Quiz]:
        """Read all quizzes from the database that a specific user has taken.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[Quiz]: The list of quizzes that the user has taken.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.user_id == user_id)
                .order_by(self.data_model.quiz_id)
            )
            quizzes = results.scalars().all()
        quizzes = [Quiz.model_validate(orm_object_to_dict(quiz)) for quiz in quizzes]
        return quizzes

    async def read_by_deck_id(self, deck_id: int) -> list[Quiz]:
        """Read all quizzes from the database that were based on a specific deck.

        Args:
            deck_id (int): The unique identifier for the deck.

        Returns:
            list[Quiz]: The list of quizzes that were based on the deck.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.deck_id == deck_id)
                .order_by(self.data_model.quiz_id)
            )
            quizzes = results.scalars().all()
        quizzes = [Quiz.model_validate(orm_object_to_dict(quiz)) for quiz in quizzes]
        return quizzes
