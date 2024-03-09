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

pytestmark = pytest.mark.anyio


class TestBaseRepositorySuccess:
    """Test cases for the `BaseRepository` class when successful."""

    # Create all domain models for testing.
    user_domain_models = (
        User(
            user_id=1,
            user_name="dummy_user1",
            email="dummy_email1",
            password="dummy_password1",
        ),
        User(
            user_id=2,
            user_name="dummy_user2",
            email="dummy_email2",
            password="dummy_password2",
        ),
    )
    user_login_history_domain_models = (
        UserLoginHistory(
            user_login_history_id=1,
            user_id=1,
            ip_address="127.0.0.1",
        ),
    )
    item_domain_models = (
        Item(
            item_id=1,
            user_id=1,
            english="dummy_english1",
            japanese="dummy_japanese1",
            grade=1,
        ),
        Item(
            item_id=2,
            user_id=1,
            english="dummy_english2",
            japanese="dummy_japanese2",
            grade=3,
        ),
        Item(
            item_id=3,
            user_id=1,
            english="dummy_english3",
            japanese="dummy_japanese3",
            grade=4,
        ),
        Item(
            item_id=4,
            user_id=1,
            english="dummy_english4",
            japanese="dummy_japanese4",
            grade=2,
        ),
    )
    deck_domain_models = (
        Deck(
            deck_id=1,
            user_id=1,
            deck_name="dummy_deck1",
        ),
    )
    quiz_domain_models = (
        Quiz(
            quiz_id=1,
            user_id=1,
            deck_id=1,
            quiz_type="dummy_quiz_type",
        ),
    )
    quiz_item_domain_models = (
        QuizItem(
            quiz_item_id=1,
            quiz_id=1,
            item_id=1,
            question_number=1,
            choice_item_ids=[1, 2, 3, 4],
            correct_answer=0,
            user_answer=0,
            answer_time=10,
        ),
    )

    async def test_create(self, async_db_session: AsyncSession) -> None:
        """Test the `BaseRepository.create` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
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
        user = await user_repository.create(self.user_domain_models[0])
        user_login_history = await user_login_history_repository.create(
            self.user_login_history_domain_models[0]
        )
        item1 = await item_repository.create(self.item_domain_models[0])
        item2 = await item_repository.create(self.item_domain_models[1])
        item3 = await item_repository.create(self.item_domain_models[2])
        item4 = await item_repository.create(self.item_domain_models[3])
        deck = await deck_repository.create(self.deck_domain_models[0])
        quiz = await quiz_repository.create(self.quiz_domain_models[0])
        quiz_item = await quiz_item_repository.create(self.quiz_item_domain_models[0])
        # Test if the returned data are correct (i.e. equals to the ones created above).
        assert user == self.user_domain_models[0]
        assert user_login_history == self.user_login_history_domain_models[0]
        assert item1 == self.item_domain_models[0]
        assert item2 == self.item_domain_models[1]
        assert item3 == self.item_domain_models[2]
        assert item4 == self.item_domain_models[3]
        assert deck == self.deck_domain_models[0]
        assert quiz == self.quiz_domain_models[0]
        assert quiz_item == self.quiz_item_domain_models[0]

    async def test_read(self, async_db_session: AsyncSession) -> None:
        """Test the `BaseRepository.read` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        # Create all data models for testing.
        user_data_model = SQLAlchemyUser(**self.user_domain_models[0].model_dump())
        user_login_history_data_model = SQLAlchemyUserLoginHistory(
            **self.user_login_history_domain_models[0].model_dump()
        )
        item1_data_model = SQLAlchemyItem(**self.item_domain_models[0].model_dump())
        item2_data_model = SQLAlchemyItem(**self.item_domain_models[1].model_dump())
        item3_data_model = SQLAlchemyItem(**self.item_domain_models[2].model_dump())
        item4_data_model = SQLAlchemyItem(**self.item_domain_models[3].model_dump())
        deck_data_model = SQLAlchemyDeck(**self.deck_domain_models[0].model_dump())
        quiz_data_model = SQLAlchemyQuiz(**self.quiz_domain_models[0].model_dump())
        quiz_item_data_model = SQLAlchemyQuizItem(
            **self.quiz_item_domain_models[0].model_dump()
        )
        async with async_db_session.begin():
            async_db_session.add_all(
                [
                    user_data_model,
                    user_login_history_data_model,
                    item1_data_model,
                    item2_data_model,
                    item3_data_model,
                    item4_data_model,
                    deck_data_model,
                    quiz_data_model,
                    quiz_item_data_model,
                ]
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
        # Get each data by ID.
        user = await user_repository.read(id=1)
        user_login_history = await user_login_history_repository.read(id=1)
        item1 = await item_repository.read(id=1)
        item2 = await item_repository.read(id=2)
        item3 = await item_repository.read(id=3)
        item4 = await item_repository.read(id=4)
        deck = await deck_repository.read(id=1)
        quiz = await quiz_repository.read(id=1)
        quiz_item = await quiz_item_repository.read(id=1)
        # Test if the returned data are correct (i.e. equals to the ones created above).
        assert user == self.user_domain_models[0]
        assert user_login_history == self.user_login_history_domain_models[0]
        assert item1 == self.item_domain_models[0]
        assert item2 == self.item_domain_models[1]
        assert item3 == self.item_domain_models[2]
        assert item4 == self.item_domain_models[3]
        assert deck == self.deck_domain_models[0]
        assert quiz == self.quiz_domain_models[0]
        assert quiz_item == self.quiz_item_domain_models[0]

    async def test_update(self, async_db_session: AsyncSession) -> None:
        """Test the `BaseRepository.update` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        # Create all domain/data models for testing.
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
        user_data_model = SQLAlchemyUser(**self.user_domain_models[0].model_dump())
        user_login_history_data_model = SQLAlchemyUserLoginHistory(
            **self.user_login_history_domain_models[0].model_dump()
        )
        item1_data_model = SQLAlchemyItem(**self.item_domain_models[0].model_dump())
        item2_data_model = SQLAlchemyItem(**self.item_domain_models[1].model_dump())
        item3_data_model = SQLAlchemyItem(**self.item_domain_models[2].model_dump())
        item4_data_model = SQLAlchemyItem(**self.item_domain_models[3].model_dump())
        deck_data_model = SQLAlchemyDeck(**self.deck_domain_models[0].model_dump())
        quiz_data_model = SQLAlchemyQuiz(**self.quiz_domain_models[0].model_dump())
        quiz_item_data_model = SQLAlchemyQuizItem(
            **self.quiz_item_domain_models[0].model_dump()
        )
        async with async_db_session.begin():
            async_db_session.add_all(
                [
                    user_data_model,
                    user_login_history_data_model,
                    item1_data_model,
                    item2_data_model,
                    item3_data_model,
                    item4_data_model,
                    deck_data_model,
                    quiz_data_model,
                    quiz_item_data_model,
                ]
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

    async def test_delete(self, async_db_session: AsyncSession) -> None:
        """Test the `BaseRepository.delete` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        # Create a user for testing.
        user_domain_model = User(
            user_id=1,
            user_name="dummy_user",
            email="dummy_email",
            password="dummy_password",
        )
        user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
        async with async_db_session.begin():
            async_db_session.add(user_data_model)

        # Instantiate the `UserRepository` class.
        user_repository = BaseRepository[SQLAlchemyUser, User](
            SQLAlchemyUser, User, async_db_session
        )
        # Delete the user.
        await user_repository.delete(id=1)
        # Test if the user is deleted.
        with pytest.raises(ValueError):
            await user_repository.read(id=1)
