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

@pytest.mark.usefixtures("assingn_authenticated_async_test_client_to_class")
class TestDeckRoutes:
    fixture_overridden_attribute_names: list[str] | None = ["client"]

    async def test_deck_get(self):
        print(self.client.build_request("GET", "/decks/").url)
        response = await self.client.get("/decks/")
        assert response.status_code == 200
        assert response.json() == [{"deck_id": 1, "deck_name": "dummy_deck"}]

    async def test_deck_post(self):
        print(self.client.build_request("POST", "/decks/").url)
        response = await self.client.post("/decks/")
        assert response.status_code == 200
        assert response.json() == {"deck_id": 1, "deck_name": "dummy_deck"}