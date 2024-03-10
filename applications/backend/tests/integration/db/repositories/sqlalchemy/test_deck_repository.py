import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyDeck, SQLAlchemyUser
from src.db.repositories.sqlalchemy.deck_repository import DeckRepository
from src.domain.models import Deck, User
from tests.utils import DomainModelDict

pytestmark = pytest.mark.anyio


class TestDeckRepositorySuccess:
    """Test cases for the `DeckRepository` class when successful."""

    async def test_real_all(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `DeckRepository.read_all` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `DeckRepository` class.
        deck_repository = DeckRepository(async_db_session)
        # Get all the decks.
        decks = await deck_repository.read_all()
        # Test if the returned decks are correct (i.e. equals to the ones created above).
        assert len(decks) == 3
        assert decks[0] == domain_model_dict["deck_domain_models"][0]
        assert decks[1] == domain_model_dict["deck_domain_models"][1]
        assert decks[2] == domain_model_dict["deck_domain_models"][2]

    async def test_read_by_user_id(self, repository_class_provision: tuple[AsyncSession, DomainModelDict]) -> None:
        """Test the `DeckRepository.read_by_user_id` method.

        Args:
            async_db_session (AsyncSession): An asynchronous database session.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `DeckRepository` class.
        deck_repository = DeckRepository(async_db_session)
        # Get the decks of user1 and user2.
        user1_decks = await deck_repository.read_by_user_id(user_id=1)
        user2_decks = await deck_repository.read_by_user_id(user_id=2)
        # Test if the returned decks are correct (i.e. equals to the ones created above).
        assert len(user1_decks) == 2
        assert user1_decks[0] == domain_model_dict["deck_domain_models"][0]
        assert user1_decks[1] == domain_model_dict["deck_domain_models"][1]
        assert len(user2_decks) == 1
        assert user2_decks[0] == domain_model_dict["deck_domain_models"][2]
