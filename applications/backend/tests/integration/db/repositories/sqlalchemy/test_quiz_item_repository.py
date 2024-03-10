import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.sqlalchemy.quiz_item_repository import QuizItemRepository
from tests.utils import DomainModelDict

pytestmark = pytest.mark.anyio


class TestQuizItemRepositorySuccess:
    """Test cases for the `QuizItemRepository` class when successful."""

    async def test_read_by_user_id(
        self, repository_class_provision: tuple[AsyncSession, DomainModelDict]
    ) -> None:
        """Test the `QuizItemRepository.read_by_quiz_id` method.

        Args:
            repository_class_provision (tuple[AsyncSession, DomainModelDict]):
                A tuple of an asynchronous database session and a dictionary of prepared domain models.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `QuizItemRepository` class.
        quiz_item_repository = QuizItemRepository(async_db_session)
        # Get the items of quiz1 and quiz2.
        quiz1_items = await quiz_item_repository.read_by_quiz_id(quiz_id=1)
        quiz2_items = await quiz_item_repository.read_by_quiz_id(quiz_id=2)
        quiz3_items = await quiz_item_repository.read_by_quiz_id(quiz_id=3)
        # Test if the returned items are correct (i.e. equals to the ones created above).
        assert len(quiz1_items) == 2
        assert quiz1_items[0] == domain_model_dict["quiz_item_domain_models"][0]
        assert quiz1_items[1] == domain_model_dict["quiz_item_domain_models"][1]
        assert len(quiz2_items) == 2
        assert quiz2_items[0] == domain_model_dict["quiz_item_domain_models"][2]
        assert quiz2_items[1] == domain_model_dict["quiz_item_domain_models"][3]
        assert len(quiz3_items) == 1
        assert quiz3_items[0] == domain_model_dict["quiz_item_domain_models"][4]

    async def test_read_by_item_id(
        self, repository_class_provision: tuple[AsyncSession, DomainModelDict]
    ) -> None:
        """Test the `QuizItemRepository.read_by_item_id` method.

        Args:
            repository_class_provision (tuple[AsyncSession, DomainModelDict]):
                A tuple of an asynchronous database session and a dictionary of prepared domain models.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `QuizItemRepository` class.
        quiz_item_repository = QuizItemRepository(async_db_session)
        # Get the quiz items asking for item1 and item2.
        item1_quiz_items = await quiz_item_repository.read_by_item_id(item_id=1)
        item2_quiz_items = await quiz_item_repository.read_by_item_id(item_id=2)
        item3_quiz_items = await quiz_item_repository.read_by_item_id(item_id=3)
        item4_quiz_items = await quiz_item_repository.read_by_item_id(item_id=4)
        # Test if the returned quiz items are correct (i.e. equals to the ones created above).
        assert len(item1_quiz_items) == 1
        assert item1_quiz_items[0] == domain_model_dict["quiz_item_domain_models"][0]
        assert len(item2_quiz_items) == 2
        assert item2_quiz_items[0] == domain_model_dict["quiz_item_domain_models"][1]
        assert item2_quiz_items[1] == domain_model_dict["quiz_item_domain_models"][3]
        assert len(item3_quiz_items) == 1
        assert item3_quiz_items[0] == domain_model_dict["quiz_item_domain_models"][2]
        assert len(item4_quiz_items) == 1
        assert item4_quiz_items[0] == domain_model_dict["quiz_item_domain_models"][4]
