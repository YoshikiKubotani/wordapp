import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import SQLAlchemyItem, SQLAlchemyUser
from src.db.repositories.sqlalchemy.item_repository import ItemRepository
from src.domain.models import Item, User

pytestmark = pytest.mark.anyio


async def test_read_by_user_id(async_db_session: AsyncSession) -> None:
    """Test the `ItemRepository.read_by_user_id` method.

    Args:
        async_db_session (AsyncSession): An asynchronous database session.
    """
    # Create two users and three items for testing.
    user1_domain_model = User(
        user_id=1,
        user_name="dummy_user1",
        email="dummy_email1",
        password="dummy_password1",
    )
    user2_domain_model = User(
        user_id=2,
        user_name="dummy_user2",
        email="dummy_email2",
        password="dummy_password2",
    )
    item1_domain_model = Item(
        item_id=1,
        user_id=1,
        english="dummy_english1",
        japanese="dummy_japanese1",
        grade=1,
    )
    item2_domain_model = Item(
        item_id=2,
        user_id=1,
        english="dummy_english2",
        japanese="dummy_japanese2",
        grade=2,
    )
    item3_domain_model = Item(
        item_id=3,
        user_id=2,
        english="dummy_english3",
        japanese="dummy_japanese3",
        grade=3,
    )
    user1_data_model = SQLAlchemyUser(**user1_domain_model.model_dump())
    user2_data_model = SQLAlchemyUser(**user2_domain_model.model_dump())
    item1_data_model = SQLAlchemyItem(**item1_domain_model.model_dump())
    item2_data_model = SQLAlchemyItem(**item2_domain_model.model_dump())
    item3_data_model = SQLAlchemyItem(**item3_domain_model.model_dump())
    async with async_db_session.begin():
        async_db_session.add_all(
            [
                user1_data_model,
                user2_data_model,
                item1_data_model,
                item2_data_model,
                item3_data_model,
            ]
        )
        await async_db_session.flush()

    # Instantiate the `ItemRepository` class.
    item_repository = ItemRepository(async_db_session)
    # Get the items of user1 and user2.
    user1_items = await item_repository.read_by_user_id(user_id=1)
    user2_items = await item_repository.read_by_user_id(user_id=2)
    # Test if the returned items are correct (i.e. equals to the ones created above).
    assert len(user1_items) == 2
    assert user1_items[0] == item1_domain_model
    assert user1_items[1] == item2_domain_model
    assert len(user2_items) == 1
    assert user2_items[0] == item3_domain_model
