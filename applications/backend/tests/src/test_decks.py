import pytest
from httpx import AsyncClient

from src.api.routers.decks import router
from src.core.config import settings

pytestmark = pytest.mark.anyio

# @pytest.mark.anyio
# async def test_root(async_client):
#     response = await async_client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Tomato"}

@pytest.mark.usefixtures("async_client")
class TestDeckRoutes:
    async def test_root(self):
        response = await self.client.get("/")
        assert response.status_code == 200
        assert response.json() == [{"deck_id": 1, "deck_name": "dummy_deck"}]

    async def test_another_endpoint(self):
        response = await self.client.post("/")
        assert response.status_code == 200
        assert response.json() == {"deck_id": 1, "deck_name": "dummy_deck"}