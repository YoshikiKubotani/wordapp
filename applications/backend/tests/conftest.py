import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from src.core.main import app
from src.core.config import settings
server_url = f"http://localhost:8000{settings.API_V1_STR}/"

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="class")
async def async_client(request):
    """Generate an async client for testing with lifespan manager.

    This ensures the lifespan manager to provide the database session factory before the test,
    and then close the engine after the test.
    """
    async with LifespanManager(app) as manager:
      async with AsyncClient(app=manager.app, base_url=server_url) as client:
        # If the test class has attrubutes to override, do it here.
        if hasattr(request.cls, "fixture_overridden_attribute_names"):
            # Only override the client attribute.
            for attr in request.cls.fixture_overridden_attribute_names:
                if attr == "client":
                  setattr(request.cls, attr, client)



# # AsyncClient のフィクスチャを定義
# @pytest.fixture(scope="class")
# async def async_client(request):
#     client = AsyncClient(app=app, base_url=settings.API_V1_STR)
#     if request.cls is not None:
#         request.cls.client = client
#     yield client
#     await client.aclose()