from sqlalchemy import select

from new_src.db.repositories.base_repository import BaseRepository, AsyncSessionDep
from new_src.db.data_models import Item
from new_src.api.schemas import ItemSchema

class ItemRepository(BaseRepository[Item, ItemSchema]):
  def __init__(self) -> None:
    super().__init__(data_model=Item)
      
  async def read_by_user_id(self, async_session: AsyncSessionDep, user_id: int) -> list[ItemSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        items = await session.execute(select(self.data_model).where(self.data_model.user_id == user_id))
        return items.scalars().all()