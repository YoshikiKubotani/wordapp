from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyItem, orm_object_to_dict
from src.domain.models import Item
from src.db.repositories.item_repository_interface import IItemRepository

from .base_repository import BaseRepository


class ItemRepository(BaseRepository[SQLAlchemyItem, Item], IItemRepository):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(
            data_model=SQLAlchemyItem, domain_model=Item, async_seesoon=async_session
        )

    async def read_by_user_id(self, user_id: int) -> list[Item]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model)
                .where(self.data_model.user_id == user_id)
                .order_by(self.data_model.item_id)
            )
            items = results.scalars().all()
        items = [Item.model_validate(orm_object_to_dict(item)) for item in items]
        return items
