from sqlalchemy import select

from new_src.api.schemas import TestItemSchema
from new_src.db.data_models import TestItem
from new_src.db.repositories.base_repository import AsyncSessionDep, BaseRepository


class TestItemRepository(BaseRepository[TestItem, TestItemSchema]):
  def __init__(self) -> None:
    super().__init__(data_model=TestItem)
  
  async def read_by_test_id(self, async_session: AsyncSessionDep, test_id: int) -> list[TestItemSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        test_items = await session.execute(select(self.data_model).where(self.data_model.test_id == test_id))
        return test_items.scalars().all()
      
  async def read_by_item_id(self, async_session: AsyncSessionDep, item_id: int) -> list[TestItemSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        test_items = await session.execute(select(self.data_model).where(self.data_model.item_id == item_id))
        return test_items.scalars().all()