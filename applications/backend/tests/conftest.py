from typing import Any

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from src.core.config import settings
from src.core.main import app

server_url = f"http://localhost:8000{settings.API_V1_STR}/"
test_user = "botany"
test_password = "kubotani"


def setup_class_attributes(target_cls: Any, config: dict[str, str]) -> set[str]:
    found_attributes: set = set()
    if hasattr(target_cls, "fixture_overridden_attribute_names"):
        for attribute in target_cls.fixture_overridden_attribute_names:
            if attribute in config:
                setattr(target_cls, attribute, config[attribute])
                found_attributes.add(attribute)
    unfound_attributes = set(config.keys()) - found_attributes
    return unfound_attributes


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def lifespan_manager():
    async with LifespanManager(app) as manager:
        yield manager


@pytest.fixture(scope="session")
async def async_db_session(lifespan_manager):
    from src.core.main import AsyncSessionFactory

    async with AsyncSessionFactory() as session:
        yield session


@pytest.fixture(scope="class")
async def async_test_client(lifespan_manager):
    async with AsyncClient(app=lifespan_manager.app, base_url=server_url) as client:
        yield client


@pytest.fixture(scope="class")
async def authenticated_async_test_client(async_test_client):
    """Create an authenticated user for testing."""
    response = await async_test_client.post(
        "/login/access-token",
        data={"username": test_user, "password": test_password},
    )
    print("response", response.json())
    token = response.json()["access_token"]
    token_type = response.json()["token_type"]
    async_test_client.headers = {"Authorization": f"{token_type} {token}"}
    yield async_test_client


@pytest.fixture(scope="class")
async def assingn_authenticated_async_test_client_to_class(
    request, authenticated_async_test_client
):
    """Assign the authenticated client to the class.

    This is used to override the client fixture in the test class.
    """
    unfound_attributes = setup_class_attributes(
        request.cls, {"client": authenticated_async_test_client}
    )
    if "client" in unfound_attributes:
        raise ValueError(
            'The test class must have "fixture_overridden_attribute_names" attribute which contains "client" to assign authenticated async test client.'
        )
    yield
