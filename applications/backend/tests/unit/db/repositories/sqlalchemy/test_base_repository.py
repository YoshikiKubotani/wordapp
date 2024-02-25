import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import AliasChoices, BaseModel, Field
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.db.models.sqlalchemy_data_models import (
  SQLAlchemyDeck,
  SQLAlchemyQuiz,
  SQLAlchemyQuizItem,
  SQLAlchemyItem,
  SQLAlchemyUser,
  SQLAlchemyUserLoginHistory,
)
from src.db.repositories.sqlalchemy.base_repository import BaseRepository
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import Deck, Quiz, QuizItem, Item, User, UserLoginHistory

pytestmark = pytest.mark.anyio

async def test_create(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.create` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create all domain models for testing.
    user_domain_model = User(
        user_id=1,
        user_name="dummy_user",
        email="dummy_email",
        password="dummy_password",
    )
    user_login_history_domain_model = UserLoginHistory(
        user_login_history_id=1,
        user_id=1,
        ip_address="127.0.0.1",
    )
    item1_domain_model = Item(
        item_id=1,
        user_id=1,
        english="dummy_english1",
        japanese="dummy_japanese1",
        grade=1,
    )
    item2_domain_model = Item(
        item_id=2,
        user_id=1,
        english="dummy_english2",
        japanese="dummy_japanese2",
        grade=2,
    )
    item3_domain_model = Item(
        item_id=3,
        user_id=1,
        english="dummy_english3",
        japanese="dummy_japanese3",
        grade=3,
    )
    item4_domain_model = Item(
        item_id=4,
        user_id=1,
        english="dummy_english4",
        japanese="dummy_japanese4",
        grade=4,
    )
    deck_domain_model = Deck(
        deck_id=1,
        user_id=1,
        deck_name="dummy_deck",
    )
    quiz_domain_model = Quiz(
        quiz_id=1,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type",
    )
    quiz_item_domain_model = QuizItem(
        quiz_item_id=1,
        quiz_id=1,
        item_id=1,
        question_number=1,
        choice_item_ids=[1,2,3,4],
        correct_answer=0,
        user_answer=0,
        answer_time=10,
    )

    # Instantiate the `BaseRepository` class.
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    user_login_history_repository = BaseRepository[SQLAlchemyUserLoginHistory, UserLoginHistory](SQLAlchemyUserLoginHistory, UserLoginHistory, async_db_session)
    item_repository = BaseRepository[SQLAlchemyItem, Item](SQLAlchemyItem, Item, async_db_session)
    deck_repository = BaseRepository[SQLAlchemyDeck, Deck](SQLAlchemyDeck, Deck, async_db_session)
    quiz_repository = BaseRepository[SQLAlchemyQuiz, Quiz](SQLAlchemyQuiz, Quiz, async_db_session)
    quiz_item_repository = BaseRepository[SQLAlchemyQuizItem, QuizItem](SQLAlchemyQuizItem, QuizItem, async_db_session)
    # Create each domain model (note: order sensitive).
    user = await user_repository.create(user_domain_model)
    user_login_history = await user_login_history_repository.create(user_login_history_domain_model)
    item1 = await item_repository.create(item1_domain_model)
    item2 = await item_repository.create(item2_domain_model)
    item3 = await item_repository.create(item3_domain_model)
    item4 = await item_repository.create(item4_domain_model)
    deck = await deck_repository.create(deck_domain_model)
    quiz = await quiz_repository.create(quiz_domain_model)
    quiz_item = await quiz_item_repository.create(quiz_item_domain_model)
    # Test if the returned data are correct (i.e. equals to the ones created above).
    assert user == user_domain_model
    assert user_login_history == user_login_history_domain_model
    assert item1 == item1_domain_model
    assert item2 == item2_domain_model
    assert item3 == item3_domain_model
    assert item4 == item4_domain_model
    assert deck == deck_domain_model
    assert quiz == quiz_domain_model
    assert quiz_item == quiz_item_domain_model

async def test_read(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.read` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create all domain/data models for testing.
    user_domain_model = User(
        user_id=1,
        user_name="dummy_user",
        email="dummy_email",
        password="dummy_password",
    )
    user_login_history_domain_model = UserLoginHistory(
        user_login_history_id=1,
        user_id=1,
        ip_address="127.0.0.1",
    )
    item1_domain_model = Item(
        item_id=1,
        user_id=1,
        english="dummy_english1",
        japanese="dummy_japanese1",
        grade=1,
    )
    item2_domain_model = Item(
        item_id=2,
        user_id=1,
        english="dummy_english2",
        japanese="dummy_japanese2",
        grade=2,
    )
    item3_domain_model = Item(
        item_id=3,
        user_id=1,
        english="dummy_english3",
        japanese="dummy_japanese3",
        grade=3,
    )
    item4_domain_model = Item(
        item_id=4,
        user_id=1,
        english="dummy_english4",
        japanese="dummy_japanese4",
        grade=4,
    )
    deck_domain_model = Deck(
        deck_id=1,
        user_id=1,
        deck_name="dummy_deck",
    )
    quiz_domain_model = Quiz(
        quiz_id=1,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type",
    )
    quiz_item_domain_model = QuizItem(
        quiz_item_id=1,
        quiz_id=1,
        item_id=1,
        question_number=1,
        choice_item_ids=[1,2,3,4],
        correct_answer=0,
        user_answer=0,
        answer_time=10,
    )
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    user_login_history_data_model = SQLAlchemyUserLoginHistory(**user_login_history_domain_model.model_dump())
    item1_data_model = SQLAlchemyItem(**item1_domain_model.model_dump())
    item2_data_model = SQLAlchemyItem(**item2_domain_model.model_dump())
    item3_data_model = SQLAlchemyItem(**item3_domain_model.model_dump())
    item4_data_model = SQLAlchemyItem(**item4_domain_model.model_dump())
    deck_data_model = SQLAlchemyDeck(**deck_domain_model.model_dump())
    quiz_data_model = SQLAlchemyQuiz(**quiz_domain_model.model_dump())
    quiz_item_data_model = SQLAlchemyQuizItem(**quiz_item_domain_model.model_dump())
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
        await async_db_session.flush()

    # Instantiate the `BaseRepository` class.
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    user_login_history_repository = BaseRepository[SQLAlchemyUserLoginHistory, UserLoginHistory](SQLAlchemyUserLoginHistory, UserLoginHistory, async_db_session)
    item_repository = BaseRepository[SQLAlchemyItem, Item](SQLAlchemyItem, Item, async_db_session)
    deck_repository = BaseRepository[SQLAlchemyDeck, Deck](SQLAlchemyDeck, Deck, async_db_session)
    quiz_repository = BaseRepository[SQLAlchemyQuiz, Quiz](SQLAlchemyQuiz, Quiz, async_db_session)
    quiz_item_repository = BaseRepository[SQLAlchemyQuizItem, QuizItem](SQLAlchemyQuizItem, QuizItem, async_db_session)
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
    assert user == user_domain_model
    assert user_login_history == user_login_history_domain_model
    assert item1 == item1_domain_model
    assert item2 == item2_domain_model
    assert item3 == item3_domain_model
    assert item4 == item4_domain_model
    assert deck == deck_domain_model
    assert quiz == quiz_domain_model
    assert quiz_item == quiz_item_domain_model

async def test_update(async_db_session: AsyncSession) -> None:
    """Test the `BaseRepository.update` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create all domain/data models for testing.
    user_domain_model = User(
        user_id=1,
        user_name="dummy_user",
        email="dummy_email",
        password="dummy_password",
    )
    user_login_history_domain_model = UserLoginHistory(
        user_login_history_id=1,
        user_id=1,
        ip_address="127.0.0.1",
    )
    item1_domain_model = Item(
        item_id=1,
        user_id=1,
        english="dummy_english1",
        japanese="dummy_japanese1",
        grade=1,
    )
    item2_domain_model = Item(
        item_id=2,
        user_id=1,
        english="dummy_english2",
        japanese="dummy_japanese2",
        grade=2,
    )
    item3_domain_model = Item(
        item_id=3,
        user_id=1,
        english="dummy_english3",
        japanese="dummy_japanese3",
        grade=3,
    )
    item4_domain_model = Item(
        item_id=4,
        user_id=1,
        english="dummy_english4",
        japanese="dummy_japanese4",
        grade=4,
    )
    deck_domain_model = Deck(
        deck_id=1,
        user_id=1,
        deck_name="dummy_deck",
    )
    quiz_domain_model = Quiz(
        quiz_id=1,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type",
    )
    quiz_item_domain_model = QuizItem(
        quiz_item_id=1,
        quiz_id=1,
        item_id=1,
        question_number=1,
        choice_item_ids=[1,2,3,4],
        correct_answer=0,
        user_answer=0,
        answer_time=10,
    )
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
        choice_item_ids=[2,1,3,4],
        correct_answer=1,
        user_answer=0,
        answer_time=10,
    )
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    user_login_history_data_model = SQLAlchemyUserLoginHistory(**user_login_history_domain_model.model_dump())
    item1_data_model = SQLAlchemyItem(**item1_domain_model.model_dump())
    item2_data_model = SQLAlchemyItem(**item2_domain_model.model_dump())
    item3_data_model = SQLAlchemyItem(**item3_domain_model.model_dump())
    item4_data_model = SQLAlchemyItem(**item4_domain_model.model_dump())
    deck_data_model = SQLAlchemyDeck(**deck_domain_model.model_dump())
    quiz_data_model = SQLAlchemyQuiz(**quiz_domain_model.model_dump())
    quiz_item_data_model = SQLAlchemyQuizItem(**quiz_item_domain_model.model_dump())
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
        await async_db_session.flush()

    # Instantiate the `BaseRepository` class.
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    user_login_history_repository = BaseRepository[SQLAlchemyUserLoginHistory, UserLoginHistory](SQLAlchemyUserLoginHistory, UserLoginHistory, async_db_session)
    item_repository = BaseRepository[SQLAlchemyItem, Item](SQLAlchemyItem, Item, async_db_session)
    deck_repository = BaseRepository[SQLAlchemyDeck, Deck](SQLAlchemyDeck, Deck, async_db_session)
    quiz_repository = BaseRepository[SQLAlchemyQuiz, Quiz](SQLAlchemyQuiz, Quiz, async_db_session)
    quiz_item_repository = BaseRepository[SQLAlchemyQuizItem, QuizItem](SQLAlchemyQuizItem, QuizItem, async_db_session)
    # Update each data.
    user = await user_repository.update(updated_user_domain_model)
    user_login_history = await user_login_history_repository.update(updated_user_login_history_domain_model)
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

async def test_delete(async_db_session: AsyncSession) -> None:
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
    user_repository = BaseRepository[SQLAlchemyUser, User](SQLAlchemyUser, User, async_db_session)
    # Delete the user.
    await user_repository.delete(id=1)
    # Test if the user is deleted.
    with pytest.raises(ValueError):
        await user_repository.read(id=1)