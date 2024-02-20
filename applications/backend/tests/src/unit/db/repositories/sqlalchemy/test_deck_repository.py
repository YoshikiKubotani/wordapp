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
    test_user_domain_model = User(user_id=1, user_name="dummy_user", email="dummy_email", password="dummy_password")
    deck1_domain_model = Deck(deck_id=1, user_id=1, deck_name="dummy_deck")
    deck2_domain_model = Deck(deck_id=2, user_id=1, deck_name="dummy_deck")
    test_user_data_model = SQLAlchemyUser(**test_user_domain_model.model_dump())
    deck1_data_model = SQLAlchemyDeck(**deck1_domain_model.model_dump())
    deck2_data_model = SQLAlchemyDeck(**deck2_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add_all([deck1_data_model, deck2_data_model, test_user_data_model])
        await async_db_session.flush()

    # Test the `DeckRepository.read_all` method.
    deck_repository = DeckRepository(async_db_session)
    decks = await deck_repository.read_all()
    assert len(decks) == 2
    assert deck1_domain_model == decks[0]
    assert deck2_domain_model == decks[1]