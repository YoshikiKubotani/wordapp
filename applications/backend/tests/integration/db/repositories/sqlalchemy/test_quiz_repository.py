import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.sqlalchemy.quiz_repository import QuizRepository
from tests.utils import DomainModelDict

pytestmark = pytest.mark.anyio


class TestQuizRepositorySuccess:
    """Test cases for the `QuizRepository` class when successful."""

    async def test_read_by_user_id(
        self, repository_class_provision: tuple[AsyncSession, DomainModelDict]
    ) -> None:
        """Test the `QuizRepository.read_by_user_id` method.

        Args:
            repository_class_provision (tuple[AsyncSession, DomainModelDict]):
                A tuple of an asynchronous database session and a dictionary of prepared domain models.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `QuizRepository` class.
        quiz_repository = QuizRepository(async_db_session)
        # Get the quizzes by user_id.
        user1_quizzes = await quiz_repository.read_by_user_id(user_id=1)
        user2_quizzes = await quiz_repository.read_by_user_id(user_id=2)
        # Test if the returned quizzes are correct (i.e. equals to the ones created above).
        assert len(user1_quizzes) == 2
        assert user1_quizzes[0] == domain_model_dict["quiz_domain_models"][0]
        assert user1_quizzes[1] == domain_model_dict["quiz_domain_models"][1]
        assert len(user2_quizzes) == 1
        assert user2_quizzes[0] == domain_model_dict["quiz_domain_models"][2]

    async def test_read_by_deck_id(
        self, repository_class_provision: tuple[AsyncSession, DomainModelDict]
    ) -> None:
        """Test the `QuizRepository.read_by_deck_id` method.

        Args:
            repository_class_provision (tuple[AsyncSession, DomainModelDict]):
                A tuple of an asynchronous database session and a dictionary of prepared domain models.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `QuizRepository` class.
        quiz_repository = QuizRepository(async_db_session)
        # Get the quizzes by deck_id.
        deck1_quizzes = await quiz_repository.read_by_deck_id(deck_id=1)
        deck2_quizzes = await quiz_repository.read_by_deck_id(deck_id=2)
        # Test if the returned quizzes are correct (i.e. equals to the ones created above).
        assert len(deck1_quizzes) == 1
        assert deck1_quizzes[0] == domain_model_dict["quiz_domain_models"][0]
        assert len(deck2_quizzes) == 2
        assert deck2_quizzes[0] == domain_model_dict["quiz_domain_models"][1]
        assert deck2_quizzes[1] == domain_model_dict["quiz_domain_models"][2]
