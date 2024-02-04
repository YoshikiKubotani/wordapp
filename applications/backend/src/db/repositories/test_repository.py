from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import TestSchema
from src.db.data_models import Test
from src.db.repositories.base_repository import BaseRepository


class TestRepository(BaseRepository[Test, TestSchema]):
  def __init__(self) -> None:
    super().__init__(data_model=Test)

  async def read_by_user_id(self, async_session: AsyncSession, user_id: int) -> list[TestSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        tests = await session.execute(select(self.data_model).where(self.data_model.user_id == user_id))
        return tests.scalars().all()

  async def read_by_deck_id(self, async_session: AsyncSession, deck_id: int) -> list[TestSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        tests = await session.execute(select(self.data_model).where(self.data_model.deck_id == deck_id))
        return tests.scalars().all()