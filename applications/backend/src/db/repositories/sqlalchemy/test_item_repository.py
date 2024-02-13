from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.sqlalchemy_data_models import SQLAlchemyTestItem
from src.domain.models import TestItem

from .base_repository import BaseRepository


class TestItemRepository(BaseRepository[SQLAlchemyTestItem, TestItem]):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(data_model=SQLAlchemyTestItem, domain_model=TestItem, async_seesoon=async_session)

    async def read_by_test_id(self, test_id: int) -> list[TestItem]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            test_items = await self.async_session.execute(
                select(self.async_session).where(self.data_model.test_id == test_id)
            )
            return test_items.scalars().all()

    async def read_by_item_id(self, item_id: int) -> list[TestItem]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            test_items = await self.async_session.execute(
                select(self.data_model).where(self.data_model.item_id == item_id)
            )
            return test_items.scalars().all()
