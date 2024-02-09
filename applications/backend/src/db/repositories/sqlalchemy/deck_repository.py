from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.data_models import SQLAlchemyDeck
from src.domain.models import Deck

from .base_repository import BaseRepository


class DeckRepository(BaseRepository[SQLAlchemyDeck, Deck]):
    def __init__(self) -> None:
        super().__init__(data_model=SQLAlchemyDeck)

    async def read_all(self, async_session: AsyncSession) -> list[Deck]:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                decks = await session.execute(select(self.data_model))
                return decks.scalars().all()

    async def read_by_user_id(
        self, async_session: AsyncSession, user_id: int
    ) -> list[Deck]:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                decks = await session.execute(
                    select(self.data_model).where(self.data_model.user_id == user_id)
                )
                return decks.scalars().all()
