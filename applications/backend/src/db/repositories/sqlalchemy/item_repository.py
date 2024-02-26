from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyItem, orm_object_to_dict
from src.db.repositories.item_repository_interface import IItemRepository
from src.domain.models import Item

from .base_repository import BaseRepository


class ItemRepository(BaseRepository[SQLAlchemyItem, Item], IItemRepository):
    """The SQLAlchemy repository class for items."""

    def __init__(self, async_session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            async_session (AsyncSession): The asynchronous session to use for database operations.
        """
        super().__init__(
            data_model=SQLAlchemyItem, domain_model=Item, async_seesoon=async_session
        )

    async def read_by_user_id(self, user_id: int) -> list[Item]:
        """Read all items from the database that were made by a specific user.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            list[Item]: The list of items that were made by the user.
        """
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
