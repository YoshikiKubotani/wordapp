import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyDeck,
    SQLAlchemyQuiz,
    SQLAlchemyUser,
)
from src.db.repositories.sqlalchemy.quiz_repository import QuizRepository
from src.domain.models import Deck, Quiz, User

pytestmark = pytest.mark.anyio


class TestQuizRepositorySuccess:
    """Test cases for the `QuizRepository` class when successful."""

    async def test_read_by_user_id(self, async_db_session: AsyncSession) -> None:
        """Test the `QuizRepository.read_by_user_id` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        # Create two users, one deck, and three quizzes for testing.
        user1_domain_model = User(
            user_id=1,
            user_name="dummy_user1",
            email="dummy_email1",
            password="dummy_password1",
        )
        user2_domain_model = User(
            user_id=2,
            user_name="dummy_user2",
            email="dummy_email2",
            password="dummy_password2",
        )
        deck_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck")
        quiz1_domain_model = Quiz(
            quiz_id=1, user_id=1, deck_id=1, quiz_type="dummy_quiz_type1"
        )
        quiz2_domain_model = Quiz(
            quiz_id=2, user_id=1, deck_id=1, quiz_type="dummy_quiz_type2"
        )
        quiz3_domain_model = Quiz(
            quiz_id=3, user_id=2, deck_id=1, quiz_type="dummy_quiz_type3"
        )
        user1_data_model = SQLAlchemyUser(**user1_domain_model.model_dump())
        user2_data_model = SQLAlchemyUser(**user2_domain_model.model_dump())
        deck_data_model = SQLAlchemyDeck(**deck_domain_model.model_dump())
        quiz1_data_model = SQLAlchemyQuiz(**quiz1_domain_model.model_dump())
        quiz2_data_model = SQLAlchemyQuiz(**quiz2_domain_model.model_dump())
        quiz3_data_model = SQLAlchemyQuiz(**quiz3_domain_model.model_dump())
        async with async_db_session.begin():
            async_db_session.add_all(
                [
                    user1_data_model,
                    user2_data_model,
                    deck_data_model,
                    quiz1_data_model,
                    quiz2_data_model,
                    quiz3_data_model,
                ]
            )

        # Instantiate the `QuizRepository` class.
        quiz_repository = QuizRepository(async_db_session)
        # Get the quizzes by user_id.
        user1_quizzes = await quiz_repository.read_by_user_id(user_id=1)
        user2_quizzes = await quiz_repository.read_by_user_id(user_id=2)
        # Test if the returned quizzes are correct (i.e. equals to the ones created above).
        assert len(user1_quizzes) == 2
        assert user1_quizzes[0] == quiz1_domain_model
        assert user1_quizzes[1] == quiz2_domain_model
        assert len(user2_quizzes) == 1
        assert user2_quizzes[0] == quiz3_domain_model

    async def test_read_by_deck_id(self, async_db_session: AsyncSession) -> None:
        """Test the `QuizRepository.read_by_deck_id` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        # Create two users, one deck, and three quizzes for testing.
        user_domain_model = User(
            user_id=1,
            user_name="dummy_user",
            email="dummy_email",
            password="dummy_password",
        )
        deck1_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck1")
        deck2_domain_model = Deck(deck_id=2, user_id=1, deck_name="dummy_deck2")
        quiz1_domain_model = Quiz(
            quiz_id=1, user_id=1, deck_id=1, quiz_type="dummy_quiz_type1"
        )
        quiz2_domain_model = Quiz(
            quiz_id=2, user_id=1, deck_id=2, quiz_type="dummy_quiz_type2"
        )
        quiz3_domain_model = Quiz(
            quiz_id=3, user_id=1, deck_id=2, quiz_type="dummy_quiz_type3"
        )
        user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
        deck1_data_model = SQLAlchemyDeck(**deck1_domain_model.model_dump())
        deck2_data_model = SQLAlchemyDeck(**deck2_domain_model.model_dump())
        quiz1_data_model = SQLAlchemyQuiz(**quiz1_domain_model.model_dump())
        quiz2_data_model = SQLAlchemyQuiz(**quiz2_domain_model.model_dump())
        quiz3_data_model = SQLAlchemyQuiz(**quiz3_domain_model.model_dump())
        async with async_db_session.begin():
            async_db_session.add_all(
                [
                    user_data_model,
                    deck1_data_model,
                    deck2_data_model,
                    quiz1_data_model,
                    quiz2_data_model,
                    quiz3_data_model,
                ]
            )

        # Instantiate the `QuizRepository` class.
        quiz_repository = QuizRepository(async_db_session)
        # Get the quizzes by deck_id.
        deck1_quizzes = await quiz_repository.read_by_deck_id(deck_id=1)
        deck2_quizzes = await quiz_repository.read_by_deck_id(deck_id=2)
        # Test if the returned quizzes are correct (i.e. equals to the ones created above).
        assert len(deck1_quizzes) == 1
        assert deck1_quizzes[0] == quiz1_domain_model
        assert len(deck2_quizzes) == 2
        assert deck2_quizzes[0] == quiz2_domain_model
        assert deck2_quizzes[1] == quiz3_domain_model
