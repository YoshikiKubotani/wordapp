from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sqlalchemy_data_models import SQLAlchemyItem
from src.domain.models import Item

from .base_repository import BaseRepository


class ItemRepository(BaseRepository[SQLAlchemyItem, Item]):
    def __init__(self) -> None:
        super().__init__(data_model=SQLAlchemyItem)

    async def read_by_user_id(
        self, async_session: AsyncSession, user_id: int
    ) -> list[Item]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with async_session.begin():
            items = await async_session.execute(
                select(self.data_model).where(self.data_model.user_id == user_id)
            )
            return items.scalars().all()
