from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.sqlalchemy_data_models import SQLAlchemyTest
from src.domain.models import Test

from .base_repository import BaseRepository


class TestRepository(BaseRepository[SQLAlchemyTest, Test]):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(data_model=SQLAlchemyTest, domain_model=Test, async_seesoon=async_session)

    async def read_by_user_id(self, user_id: int) -> list[Test]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            tests = await self.async_session.execute(
                select(self.data_model).where(self.data_model.user_id == user_id)
            )
            return tests.scalars().all()

    async def read_by_deck_id(self, deck_id: int) -> list[Test]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            tests = await self.async_session.execute(
                select(self.data_model).where(self.data_model.deck_id == deck_id)
            )
            return tests.scalars().all()
