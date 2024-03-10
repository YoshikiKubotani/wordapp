import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.sqlalchemy.item_repository import ItemRepository
from tests.utils import DomainModelDict

pytestmark = pytest.mark.anyio


class TestItemRepositorySuccess:
    """Test cases for the `ItemRepository` class when successful."""

    async def test_read_by_user_id(
        self, repository_class_provision: tuple[AsyncSession, DomainModelDict]
    ) -> None:
        """Test the `ItemRepository.read_by_user_id` method.

        Args:
            repository_class_provision (tuple[AsyncSession, DomainModelDict]):
                A tuple of an asynchronous database session and a dictionary of prepared domain models.
        """
        async_db_session, domain_model_dict = repository_class_provision

        # Instantiate the `ItemRepository` class.
        item_repository = ItemRepository(async_db_session)
        # Get the items of user1 and user2.
        user1_items = await item_repository.read_by_user_id(user_id=1)
        user2_items = await item_repository.read_by_user_id(user_id=2)
        # Test if the returned items are correct (i.e. equals to the ones created above).
        assert len(user1_items) == 2
        assert user1_items[0] == domain_model_dict["item_domain_models"][0]
        assert user1_items[1] == domain_model_dict["item_domain_models"][1]
        assert len(user2_items) == 2
        assert user2_items[0] == domain_model_dict["item_domain_models"][2]
        assert user2_items[1] == domain_model_dict["item_domain_models"][3]
