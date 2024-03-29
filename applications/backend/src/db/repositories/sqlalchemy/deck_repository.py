from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyDeck, orm_object_to_dict
from src.db.repositories.deck_repository_interface import IDeckRepository
from src.domain.models import Deck

from .base_repository import BaseRepository


class DeckRepository(BaseRepository[SQLAlchemyDeck, Deck], IDeckRepository):
    """The SQLAlchemy repository class for decks."""

    def __init__(self, async_session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            async_session (AsyncSession): The asynchronous session to use for database operations.
        """
        super().__init__(
            data_model=SQLAlchemyDeck, domain_model=Deck, async_session=async_session
        )

    async def read_all(self) -> list[Deck]:
        """Read all decks from the database.

        Returns:
            list[Deck]: The list of all decks.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model).order_by(self.data_model.deck_id)
            )
            decks = results.scalars().all()
        decks = [Deck.model_validate(orm_object_to_dict(deck)) for deck in decks]
        return decks

    async def read_by_user_id(self, user_id: int) -> list[Deck]:
        """Read all decks from the database that belong to a specific user.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[Deck]: The list of decks that belong to the user.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.user_id == user_id)
                .order_by(self.data_model.deck_id)
            )
            decks = results.scalars().all()
        decks = [Deck.model_validate(orm_object_to_dict(deck)) for deck in decks]
        return decks
