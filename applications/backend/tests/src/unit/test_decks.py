import pytest

pytestmark = pytest.mark.anyio


# @pytest.mark.usefixtures("assingn_authenticated_async_test_client_to_class")
# class TestDeckRoutes:
#     fixture_overridden_attribute_names: list[str] | None = ["client"]

#     async def test_deck_get(self):
#         print(self.client.build_request("GET", "/decks/").url)
#         response = await self.client.get("/decks/")
#         assert response.status_code == 200
#         assert response.json() == [{"deck_id": 1, "deck_name": "dummy_deck"}]

#     async def test_deck_post(self):
#         print(self.client.build_request("POST", "/decks/").url)
#         response = await self.client.post("/decks/", json={"deck_name": "dummy_deck"})
#         assert response.status_code == 200
#         assert response.json() == {"deck_id": 1, "deck_name": "dummy_deck"}


async def test_deck_get(normal_async_test_client):
    print(normal_async_test_client.build_request("GET", "/decks/").url)
    response = await normal_async_test_client.get("/decks/")
    assert response.status_code == 200
    assert response.json() == [{"deck_id": 1, "deck_name": "dummy_deck"}]

async def test_deck_post(normal_async_test_client):
    print(normal_async_test_client.build_request("POST", "/decks/").url)
    response = await normal_async_test_client.post("/decks/", json={"deck_name": "dummy_deck"})
    assert response.status_code == 200
    assert response.json() == {"deck_id": 1, "deck_name": "dummy_deck"}