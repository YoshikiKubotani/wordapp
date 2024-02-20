from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyDeck, orm_object_to_dict
from src.domain.models import Deck

from .base_repository import BaseRepository


class DeckRepository(BaseRepository[SQLAlchemyDeck, Deck]):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(data_model=SQLAlchemyDeck, domain_model=Deck, async_seesoon=async_session)

    async def read_all(self) -> list[Deck]:
        # This context automatically calls async_session.close() when the code block is exited.
        async with self.async_session() as async_session:
            # This context automatically calls async_session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls async_session.rollback().
            async with async_session.begin():
                decks = await async_session.execute(select(self.data_model))
                return decks.scalars().all()

    async def read_by_user_id(self, user_id: int) -> list[Deck]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            decks = await self.async_session.execute(
                select(self.data_model).where(self.data_model.user_id == user_id)
            )
            return decks.scalars().all()
