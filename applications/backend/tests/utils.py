from typing import TypedDict
import random
import string

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.security import get_password_hash
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User, UserLoginHistory, Item, Deck, Quiz, QuizItem
from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    SQLAlchemyItem,
    SQLAlchemyDeck,
    SQLAlchemyQuiz,
    SQLAlchemyQuizItem,
)

class DomainModelDict(TypedDict):
    """A dictionary containing domain models."""
    user_domain_models: list[User]
    user_login_history_domain_models: list[UserLoginHistory]
    item_domain_models: list[Item]
    deck_domain_models: list[Deck]
    quiz_domain_models: list[Quiz]
    quiz_item_domain_models: list[QuizItem]

def random_lower_string() -> str:
    """Generate a random string of lowercase letters.

    Returns:
        str: The random string.
    """
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Generate a random email address.

    Returns:
        str: The random email address.
    """
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def create_random_test_user(async_session: AsyncSession) -> dict[str, str]:
    """Create a random normal user in the database for testing.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.

    Returns:
        dict[str, str]: The request form to log in as the created user.
    """
    user_repository = UserRepository(async_session)

    # Generate a random password.
    password = random_lower_string()

    # Check if the user already exists.
    user = await user_repository.read_by_email(settings.TEST_USER_EMAIL)
    # Create a random user if it doesn't exist.
    user_in = User(
        user_name=settings.TEST_USER_EMAIL,
        email=settings.TEST_USER_EMAIL,
        password=get_password_hash(password),
    )
    if user is None:
        print("Creating a normal user for testing.")
        user = await user_repository.create(user_in)
    else:
        print("Updating the password of the existing user for testing.")
        user = await user_repository.update(user_in)

    return {
        "username": settings.TEST_USER_EMAIL,
        "password": password,
    }


async def create_test_superuser(async_session: AsyncSession) -> dict[str, str]:
    """Create a superuser in the database for testing.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.

    Returns:
        dict[str, str]: The request form to log in as the created superuser.
    """
    user_repository = UserRepository(async_session)

    # Check if the user already exists.
    user = await user_repository.read_by_email(settings.FIRST_SUPERUSER_EMAIL)
    # Create a superuser if it doesn't exist.
    user_in = User(
        user_name=settings.FIRST_SUPERUSER,
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        is_superuser=True,
    )
    if user is None:
        print("Creating a superuser for testing.")
        user = await user_repository.create(user_in)
    else:
        print("Updating the password of the existing superuser for testing.")
        user = await user_repository.update(user_in)

    return {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }

async def prepare_data_repository_test(async_session: AsyncSession) -> DomainModelDict:
    """Prepare the data for testing the repository classes.

    Args:
        async_session (AsyncSession): The SQLAlchemy async session.

    Returns:
        DomainModelDict: The prepared domain models for testing.
    """
    # Create all domain models for testing.
    user_domain_models = [
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
    ]
    user_login_history_domain_models = [
        UserLoginHistory(
            user_login_history_id=1,
            user_id=1,
            ip_address="127.0.0.1",
        ),
        UserLoginHistory(
            user_login_history_id=2,
            user_id=1,
            ip_address="127.0.0.1",
        ),
        UserLoginHistory(
            user_login_history_id=3,
            user_id=2,
            ip_address="127.0.0.2",
        )
    ]
    item_domain_models = [
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
            user_id=2,
            english="dummy_english3",
            japanese="dummy_japanese3",
            grade=4,
        ),
        Item(
            item_id=4,
            user_id=2,
            english="dummy_english4",
            japanese="dummy_japanese4",
            grade=2,
        ),
    ]
    deck_domain_models = [
        Deck(
            deck_id=1,
            user_id=1,
            deck_name="dummy_deck1",
        ),
        Deck(
            deck_id=2,
            user_id=1,
            deck_name="dummy_deck2",
        ),
        Deck(
            deck_id=3,
            user_id=2,
            deck_name="dummy_deck3",
        ),
    ]
    quiz_domain_models = [
        Quiz(
            quiz_id=1,
            user_id=1,
            deck_id=1,
            quiz_type="dummy_quiz_type1",
        ),
        Quiz(
            quiz_id=2,
            user_id=1,
            deck_id=2,
            quiz_type="dummy_quiz_type2",
        ),
        Quiz(
            quiz_id=3,
            user_id=2,
            deck_id=2,
            quiz_type="dummy_quiz_type3",
        ),
    ]
    quiz_item_domain_models = [
        QuizItem(
            quiz_item_id=1,
            quiz_id=1,
            item_id=1,
            question_number=1,
            choice_item_ids=[1, 2, 3, 4],
            correct_answer=0,
            user_answer=2,
            answer_time=10,
        ),
        QuizItem(
            quiz_item_id=2,
            quiz_id=1,
            item_id=2,
            question_number=2,
            choice_item_ids=[2, 1, 4, 3],
            correct_answer=0,
            user_answer=3,
            answer_time=8,
        ),
        QuizItem(
            quiz_item_id=3,
            quiz_id=2,
            item_id=3,
            question_number=1,
            choice_item_ids=[1, 4, 3, 2],
            correct_answer=2,
            user_answer=2,
            answer_time=12,
        ),
        QuizItem(
            quiz_item_id=4,
            quiz_id=2,
            item_id=2,
            question_number=2,
            choice_item_ids=[1, 3, 2, 4],
            correct_answer=2,
            user_answer=1,
            answer_time=5,
        ),
        QuizItem(
            quiz_item_id=5,
            quiz_id=3,
            item_id=4,
            question_number=1,
            choice_item_ids=[4, 3, 2, 1],
            correct_answer=0,
            user_answer=0,
            answer_time=7,
        )
    ]

    user_data_models = [SQLAlchemyUser(**user_domain_model.model_dump()) for user_domain_model in user_domain_models]
    user_login_history_data_models = [SQLAlchemyUserLoginHistory(**user_login_history_domain_model.model_dump()) for user_login_history_domain_model in user_login_history_domain_models]
    item_data_models = [SQLAlchemyItem(**item_domain_model.model_dump()) for item_domain_model in item_domain_models]
    deck_data_models = [SQLAlchemyDeck(**deck_domain_model.model_dump()) for deck_domain_model in deck_domain_models]
    quiz_data_models = [SQLAlchemyQuiz(**quiz_domain_model.model_dump()) for quiz_domain_model in quiz_domain_models]
    quiz_item_data_models = [SQLAlchemyQuizItem(**quiz_item_domain_model.model_dump()) for quiz_item_domain_model in quiz_item_domain_models]
    all_data_models = user_data_models + user_login_history_data_models + item_data_models + deck_data_models + quiz_data_models + quiz_item_data_models

    async with async_session.begin():
        async_session.add_all(all_data_models)

    return DomainModelDict(
        user_domain_models=user_domain_models,
        user_login_history_domain_models=user_login_history_domain_models,
        item_domain_models=item_domain_models,
        deck_domain_models=deck_domain_models,
        quiz_domain_models=quiz_domain_models,
        quiz_item_domain_models=quiz_item_domain_models,
    )