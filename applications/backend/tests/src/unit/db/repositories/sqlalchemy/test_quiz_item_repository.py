import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyItem, SQLAlchemyUser,SQLAlchemyDeck, SQLAlchemyQuiz, SQLAlchemyQuizItem
from src.db.repositories.sqlalchemy.quiz_item_repository import QuizItemRepository
from src.domain.models import Item, Deck, User, Quiz, QuizItem

pytestmark = pytest.mark.anyio


async def test_read_by_user_id(async_db_session: AsyncSession) -> None:
    """Test the `QuizItemRepository.read_by_quiz_id` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create a user, a deck, two quizzes, four items, and four quiz items for testing.
    user_domain_model = User(
        user_id=1,
        user_name="dummy_user",
        email="dummy_email",
        password="dummy_password",
    )
    deck_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck")
    quiz1_domain_model = Quiz(
        quiz_id=1,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type1",
    )
    quiz2_domain_model = Quiz(
        quiz_id=2,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type2",
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
    quiz_item1_domain_model = QuizItem(
        quiz_item_id=1,
        quiz_id=1,
        item_id=1,
        question_number=1,
        choice_item_ids=[1, 2, 3, 4],
        correct_answer=0,
        user_answer=2,
        answer_time=10,
    )
    quiz_item2_domain_model = QuizItem(
        quiz_item_id=2,
        quiz_id=1,
        item_id=2,
        question_number=2,
        choice_item_ids=[2, 1, 4, 3],
        correct_answer=0,
        user_answer=3,
        answer_time=8,
    )
    quiz_item3_domain_model = QuizItem(
        quiz_item_id=3,
        quiz_id=2,
        item_id=3,
        question_number=1,
        choice_item_ids=[1, 4, 3, 2],
        correct_answer=2,
        user_answer=2,
        answer_time=12,
    )
    quiz_item4_domain_model = QuizItem(
        quiz_item_id=4,
        quiz_id=2,
        item_id=4,
        question_number=2,
        choice_item_ids=[1, 3, 2, 4],
        correct_answer=3,
        user_answer=1,
        answer_time=5,
    )
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    deck_data_model = SQLAlchemyDeck(**deck_domain_model.model_dump())
    quiz1_data_model = SQLAlchemyQuiz(**quiz1_domain_model.model_dump())
    quiz2_data_model = SQLAlchemyQuiz(**quiz2_domain_model.model_dump())
    item1_data_model = SQLAlchemyItem(**item1_domain_model.model_dump())
    item2_data_model = SQLAlchemyItem(**item2_domain_model.model_dump())
    item3_data_model = SQLAlchemyItem(**item3_domain_model.model_dump())
    item4_data_model = SQLAlchemyItem(**item4_domain_model.model_dump())
    quiz_item1_data_model = SQLAlchemyQuizItem(**quiz_item1_domain_model.model_dump())
    quiz_item2_data_model = SQLAlchemyQuizItem(**quiz_item2_domain_model.model_dump())
    quiz_item3_data_model = SQLAlchemyQuizItem(**quiz_item3_domain_model.model_dump())
    quiz_item4_data_model = SQLAlchemyQuizItem(**quiz_item4_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add_all(
            [
                user_data_model,
                deck_data_model,
                quiz1_data_model,
                quiz2_data_model,
                item1_data_model,
                item2_data_model,
                item3_data_model,
                item4_data_model,
                quiz_item1_data_model,
                quiz_item2_data_model,
                quiz_item3_data_model,
                quiz_item4_data_model,
            ]
        )
        await async_db_session.flush()

    # Instantiate the `QuizItemRepository` class.
    quiz_item_repository = QuizItemRepository(async_db_session)
    # Get the items of quiz1 and quiz2.
    quiz1_items = await quiz_item_repository.read_by_quiz_id(quiz_id=1)
    quiz2_items = await quiz_item_repository.read_by_quiz_id(quiz_id=2)
    # Test if the returned items are correct (i.e. equals to the ones created above).
    assert len(quiz1_items) == 2
    assert quiz1_items[0] == quiz_item1_domain_model
    assert quiz1_items[1] == quiz_item2_domain_model
    assert len(quiz2_items) == 2
    assert quiz2_items[0] == quiz_item3_domain_model
    assert quiz2_items[1] == quiz_item4_domain_model


async def test_read_by_item_id(async_db_session: AsyncSession) -> None:
    """Test the `QuizItemRepository.read_by_item_id` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create a user, a deck, two quizzes, four items, and four quiz items for testing.
    user_domain_model = User(
        user_id=1,
        user_name="dummy_user",
        email="dummy_email",
        password="dummy_password",
    )
    deck_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck")
    quiz1_domain_model = Quiz(
        quiz_id=1,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type1",
    )
    quiz2_domain_model = Quiz(
        quiz_id=2,
        user_id=1,
        deck_id=1,
        quiz_type="dummy_quiz_type2",
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
    quiz_item1_domain_model = QuizItem(
        quiz_item_id=1,
        quiz_id=1,
        item_id=1,
        question_number=1,
        choice_item_ids=[1, 2, 3, 4],
        correct_answer=0,
        user_answer=2,
        answer_time=10,
    )
    quiz_item2_domain_model = QuizItem(
        quiz_item_id=2,
        quiz_id=1,
        item_id=2,
        question_number=2,
        choice_item_ids=[2, 1, 4, 3],
        correct_answer=0,
        user_answer=3,
        answer_time=8,
    )
    quiz_item3_domain_model = QuizItem(
        quiz_item_id=3,
        quiz_id=1,
        item_id=3,
        question_number=3,
        choice_item_ids=[1, 4, 3, 2],
        correct_answer=2,
        user_answer=2,
        answer_time=12,
    )
    quiz_item4_domain_model = QuizItem(
        quiz_item_id=4,
        quiz_id=2,
        item_id=2,
        question_number=1,
        choice_item_ids=[1, 3, 2, 4],
        correct_answer=3,
        user_answer=1,
        answer_time=5,
    )
    quiz_item5_domain_model = QuizItem(
        quiz_item_id=5,
        quiz_id=2,
        item_id=4,
        question_number=2,
        choice_item_ids=[4, 3, 2, 1],
        correct_answer=0,
        user_answer=0,
        answer_time=7,
    )
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    deck_data_model = SQLAlchemyDeck(**deck_domain_model.model_dump())
    quiz1_data_model = SQLAlchemyQuiz(**quiz1_domain_model.model_dump())
    quiz2_data_model = SQLAlchemyQuiz(**quiz2_domain_model.model_dump())
    item1_data_model = SQLAlchemyItem(**item1_domain_model.model_dump())
    item2_data_model = SQLAlchemyItem(**item2_domain_model.model_dump())
    item3_data_model = SQLAlchemyItem(**item3_domain_model.model_dump())
    item4_data_model = SQLAlchemyItem(**item4_domain_model.model_dump())
    quiz_item1_data_model = SQLAlchemyQuizItem(**quiz_item1_domain_model.model_dump())
    quiz_item2_data_model = SQLAlchemyQuizItem(**quiz_item2_domain_model.model_dump())
    quiz_item3_data_model = SQLAlchemyQuizItem(**quiz_item3_domain_model.model_dump())
    quiz_item4_data_model = SQLAlchemyQuizItem(**quiz_item4_domain_model.model_dump())
    quiz_item5_data_model = SQLAlchemyQuizItem(**quiz_item5_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add_all(
            [
                user_data_model,
                deck_data_model,
                quiz1_data_model,
                quiz2_data_model,
                item1_data_model,
                item2_data_model,
                item3_data_model,
                item4_data_model,
                quiz_item1_data_model,
                quiz_item2_data_model,
                quiz_item3_data_model,
                quiz_item4_data_model,
                quiz_item5_data_model,
            ]
        )
        await async_db_session.flush()

    # Instantiate the `QuizItemRepository` class.
    quiz_item_repository = QuizItemRepository(async_db_session)
    # Get the quiz items asking for item1 and item2.
    item1_quiz_items = await quiz_item_repository.read_by_item_id(item_id=1)
    item2_quiz_items = await quiz_item_repository.read_by_item_id(item_id=2)
    item3_quiz_items = await quiz_item_repository.read_by_item_id(item_id=3)
    item4_quiz_items = await quiz_item_repository.read_by_item_id(item_id=4)
    # Test if the returned quiz items are correct (i.e. equals to the ones created above).
    assert len(item1_quiz_items) == 1
    assert item1_quiz_items[0] == quiz_item1_domain_model
    assert len(item2_quiz_items) == 2
    assert item2_quiz_items[0] == quiz_item2_domain_model
    assert item2_quiz_items[1] == quiz_item4_domain_model
    assert len(item3_quiz_items) == 1
    assert item3_quiz_items[0] == quiz_item3_domain_model
    assert len(item4_quiz_items) == 1
    assert item4_quiz_items[0] == quiz_item5_domain_model
