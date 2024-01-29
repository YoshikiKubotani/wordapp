from sqlalchemy import select

from new_src.api.schemas import DeckSchema
from new_src.db.data_models import Deck
from new_src.db.repositories.base_repository import AsyncSessionDep, BaseRepository


class DeckRepository(BaseRepository[Deck, DeckSchema]):
  def __init__(self) -> None:
    super().__init__(data_model=Deck)

  async def read_all(self, async_session: AsyncSessionDep) -> list[DeckSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        decks = await session.execute(select(self.data_model))
        return decks.scalars().all()
      
  async def read_by_user_id(self, async_session: AsyncSessionDep, user_id: int) -> list[DeckSchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        decks = await session.execute(select(self.data_model).where(self.data_model.user_id == user_id))
        return decks.scalars().all()