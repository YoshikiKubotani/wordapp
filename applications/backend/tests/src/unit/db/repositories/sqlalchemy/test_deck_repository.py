from collections.abc import AsyncIterator
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.sqlalchemy_data_models import SQLAlchemyDeck, SQLAlchemyUser, orm_object_to_dict
from src.db.repositories.sqlalchemy.deck_repository import DeckRepository
from src.domain.models import Deck, User

pytestmark = pytest.mark.anyio

async def test_real_all(async_db_session: AsyncSession) -> None:
    """Test the `DeckRepository.read_all` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create a user and two decks for tesing.
    user_domain_model = User(user_id=1, user_name="dummy_user", email="dummy_email", password="dummy_password")
    deck1_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck1")
    deck2_domain_model = Deck(deck_id=2, user_id=1, deck_name="dummy_deck2")
    user_data_model = SQLAlchemyUser(**user_domain_model.model_dump())
    deck1_data_model = SQLAlchemyDeck(**deck1_domain_model.model_dump())
    deck2_data_model = SQLAlchemyDeck(**deck2_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add_all([user_data_model, deck1_data_model, deck2_data_model])
        await async_db_session.flush()

    # Instantiate the `DeckRepository` class.
    deck_repository = DeckRepository(async_db_session)
    # Get all the decks.
    decks = await deck_repository.read_all()
    # Test if the returned decks are correct (i.e. equals to the ones created above).
    assert len(decks) == 2
    assert decks[0] == deck1_domain_model
    assert decks[1] == deck2_domain_model


async def test_read_by_user_id(async_db_session: AsyncSession) -> None:
    """Test the `DeckRepository.read_by_user_id` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create two users and three decks for testing.
    user1_domain_model = User(user_id=1, user_name="dummy_user1", email="dummy_email1", password="dummy_password1")
    user2_domain_model = User(user_id=2, user_name="dummy_user2", email="dummy_email2", password="dummy_password2")
    deck1_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck1")
    deck2_domain_model = Deck(deck_id=2, user_id=1, deck_name="dummy_deck2")
    deck3_domain_model = Deck(deck_id=3, user_id=2, deck_name="dummy_deck3")
    user1_data_model = SQLAlchemyUser(**user1_domain_model.model_dump())
    user2_data_model = SQLAlchemyUser(**user2_domain_model.model_dump())
    deck1_data_model = SQLAlchemyDeck(**deck1_domain_model.model_dump())
    deck2_data_model = SQLAlchemyDeck(**deck2_domain_model.model_dump())
    deck3_data_model = SQLAlchemyDeck(**deck3_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add_all([user1_data_model, user2_data_model, deck1_data_model, deck2_data_model, deck3_data_model])
        await async_db_session.flush()

    # Instantiate the `DeckRepository` class.
    deck_repository = DeckRepository(async_db_session)
    # Get the decks of user1 and user2.
    user1_decks = await deck_repository.read_by_user_id(user_id=1)
    user2_decks = await deck_repository.read_by_user_id(user_id=2)
    # Test if the returned decks are correct (i.e. equals to the ones created above).
    assert len(user1_decks) == 2
    assert user1_decks[0] == deck1_domain_model
    assert user1_decks[1] == deck2_domain_model
    assert len(user2_decks) == 1
    assert user2_decks[0] == deck3_domain_model