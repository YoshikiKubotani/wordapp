import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyDeck,
    SQLAlchemyItem,
    SQLAlchemyQuiz,
    SQLAlchemyQuizItem,
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
)
from src.db.repositories.sqlalchemy.base_repository import BaseRepository
from src.domain.models import Deck, Item, Quiz, QuizItem, User, UserLoginHistory
from tests.utils import DomainModelDict

pytestmark = pytest.mark.anyio


class TestBaseRepositorySuccess:
    """Test cases for the `BaseRepository` class when successful."""
    async def test_create(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `BaseRepository.create` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, _ = repository_class_provision

        # Create domain models to add.
        user_domain_model = User(
            user_id=3,
            user_name="dummy_user3",
            email="dummy_email3",
            password="dummy_password3",
        )
        user_login_history_domain_model = UserLoginHistory(
            user_login_history_id=4,
            user_id=3,
            ip_address="127.0.0.3",
        )
        deck_domain_model = Deck(
            deck_id=4,
            user_id=3,
            deck_name="dummy_deck4"
        )
        quiz_domain_model = Quiz(
            quiz_id=4,
            user_id=3,
            deck_id=4,
            quiz_type="dummy_quiz_type4",
        )
        item_domain_model = Item(
            item_id=5,
            user_id=3,
            english="dummy_english5",
            japanese="dummy_japanese5",
            grade=1,
        )
        quiz_item_domain_model = QuizItem(
            quiz_item_id=6,
            quiz_id=4,
            item_id=5,
            question_number=1,
            choice_item_ids=[5, 2, 3, 1],
            correct_answer=3,
            user_answer=3,
            answer_time=10,
        )
        # Instantiate the `BaseRepository` class.
        user_repository = BaseRepository[SQLAlchemyUser, User](
            SQLAlchemyUser, User, async_db_session
        )
        user_login_history_repository = BaseRepository[
            SQLAlchemyUserLoginHistory, UserLoginHistory
        ](SQLAlchemyUserLoginHistory, UserLoginHistory, async_db_session)
        item_repository = BaseRepository[SQLAlchemyItem, Item](
            SQLAlchemyItem, Item, async_db_session
        )
        deck_repository = BaseRepository[SQLAlchemyDeck, Deck](
            SQLAlchemyDeck, Deck, async_db_session
        )
        quiz_repository = BaseRepository[SQLAlchemyQuiz, Quiz](
            SQLAlchemyQuiz, Quiz, async_db_session
        )
        quiz_item_repository = BaseRepository[SQLAlchemyQuizItem, QuizItem](
            SQLAlchemyQuizItem, QuizItem, async_db_session
        )
        # Create each domain model (note: order sensitive).
        user = await user_repository.create(user_domain_model)
        user_login_history = await user_login_history_repository.create(
            user_login_history_domain_model
        )
        item = await item_repository.create(item_domain_model)
        deck = await deck_repository.create(deck_domain_model)
        quiz = await quiz_repository.create(quiz_domain_model)
        quiz_item = await quiz_item_repository.create(quiz_item_domain_model)
        # Test if the returned data are correct (i.e. equals to the ones created above).
        assert user == user_domain_model
        assert user_login_history == user_login_history_domain_model
        assert item == item_domain_model
        assert deck == deck_domain_model
        assert quiz == quiz_domain_model
        assert quiz_item == quiz_item_domain_model

    async def test_read(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `BaseRepository.read` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `BaseRepository` class.
        user_repository = BaseRepository[SQLAlchemyUser, User](
            SQLAlchemyUser, User, async_db_session
        )
        user_login_history_repository = BaseRepository[
            SQLAlchemyUserLoginHistory, UserLoginHistory
        ](SQLAlchemyUserLoginHistory, UserLoginHistory, async_db_session)
        item_repository = BaseRepository[SQLAlchemyItem, Item](
            SQLAlchemyItem, Item, async_db_session
        )
        deck_repository = BaseRepository[SQLAlchemyDeck, Deck](
            SQLAlchemyDeck, Deck, async_db_session
        )
        quiz_repository = BaseRepository[SQLAlchemyQuiz, Quiz](
            SQLAlchemyQuiz, Quiz, async_db_session
        )
        quiz_item_repository = BaseRepository[SQLAlchemyQuizItem, QuizItem](
            SQLAlchemyQuizItem, QuizItem, async_db_session
        )
        # Get each data by ID.
        user = await user_repository.read(id=1)
        user_login_history = await user_login_history_repository.read(id=1)
        item = await item_repository.read(id=1)
        deck = await deck_repository.read(id=1)
        quiz = await quiz_repository.read(id=1)
        quiz_item = await quiz_item_repository.read(id=1)
        # Test if the returned data are correct (i.e. equals to the ones created above).
        assert user == domain_model_dict["user_domain_models"][0]
        assert user_login_history == domain_model_dict["user_login_history_domain_models"][0]
        assert item == domain_model_dict["item_domain_models"][0]
        assert deck == domain_model_dict["deck_domain_models"][0]
        assert quiz == domain_model_dict["quiz_domain_models"][0]
        assert quiz_item == domain_model_dict["quiz_item_domain_models"][0]

    async def test_update(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `BaseRepository.update` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, _ = repository_class_provision

        # Create all domain models to update.
        updated_user_domain_model = User(
            user_id=1,
            user_name="updated_dummy_user",
            email="updated_dummy_email",
            password="updated_dummy_password",
        )
        updated_user_login_history_domain_model = UserLoginHistory(
            user_login_history_id=1,
            user_id=1,
            ip_address="127.0.0.2",
        )
        updated_item3_domain_model = Item(
            item_id=3,
            user_id=1,
            english="updated_dummy_english3",
            japanese="updated_dummy_japanese3",
            grade=3,
        )
        updated_deck_domain_model = Deck(
            deck_id=1,
            user_id=1,
            deck_name="updated_dummy_deck",
        )
        updated_quiz_domain_model = Quiz(
            quiz_id=1,
            user_id=1,
            deck_id=1,
            quiz_type="updated_dummy_quiz_type",
        )
        updated_quiz_item_domain_model = QuizItem(
            quiz_item_id=1,
            quiz_id=1,
            item_id=1,
            question_number=1,
            choice_item_ids=[2, 1, 3, 4],
            correct_answer=1,
            user_answer=0,
            answer_time=10,
        )

        # Instantiate the `BaseRepository` class.
        user_repository = BaseRepository[SQLAlchemyUser, User](
            SQLAlchemyUser, User, async_db_session
        )
        user_login_history_repository = BaseRepository[
            SQLAlchemyUserLoginHistory, UserLoginHistory
        ](SQLAlchemyUserLoginHistory, UserLoginHistory, async_db_session)
        item_repository = BaseRepository[SQLAlchemyItem, Item](
            SQLAlchemyItem, Item, async_db_session
        )
        deck_repository = BaseRepository[SQLAlchemyDeck, Deck](
            SQLAlchemyDeck, Deck, async_db_session
        )
        quiz_repository = BaseRepository[SQLAlchemyQuiz, Quiz](
            SQLAlchemyQuiz, Quiz, async_db_session
        )
        quiz_item_repository = BaseRepository[SQLAlchemyQuizItem, QuizItem](
            SQLAlchemyQuizItem, QuizItem, async_db_session
        )
        # Update each data.
        user = await user_repository.update(updated_user_domain_model)
        user_login_history = await user_login_history_repository.update(
            updated_user_login_history_domain_model
        )
        item3 = await item_repository.update(updated_item3_domain_model)
        deck = await deck_repository.update(updated_deck_domain_model)
        quiz = await quiz_repository.update(updated_quiz_domain_model)
        quiz_item = await quiz_item_repository.update(updated_quiz_item_domain_model)
        # Test if the returned updated data are correct (i.e. equals to the ones created above).
        assert user == updated_user_domain_model
        assert user_login_history == updated_user_login_history_domain_model
        assert item3 == updated_item3_domain_model
        assert deck == updated_deck_domain_model
        assert quiz == updated_quiz_domain_model
        assert quiz_item == updated_quiz_item_domain_model

    async def test_delete(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `BaseRepository.delete` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `UserRepository` class.
        user_repository = BaseRepository[SQLAlchemyUser, User](
            SQLAlchemyUser, User, async_db_session
        )
        # Delete the user.
        await user_repository.delete(id=1)
        # Test if the user is deleted.
        with pytest.raises(ValueError):
            await user_repository.read(id=1)
