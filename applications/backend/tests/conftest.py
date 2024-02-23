import pytest
from asgi_lifespan import LifespanManager

from src.core.config import settings
from src.core.main import app
from tests.utils import random_email

server_url = f"http://localhost:8000{settings.API_V1_STR}/"

settings.TEST_USER_EMAIL = random_email()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Use the asyncio backend for asynchronous testing. This is necessary to avoid processing all the tests twice."""
    return "asyncio"


@pytest.fixture(scope="session")
async def lifespan_manager() -> LifespanManager:
    """Provide a LifespanManager instance to manage the FastAPI lifespan under asynchronous testing.

    As asynchronous test clients do not execute lifespan events by default, the LifespanManager
    of `asgi-lifespan` (https://github.com/florimondmanca/asgi-lifespan#usage) is introduced.

    Yields:
        LifespanManager: An instance of LifespanManager.
    """
    # On entering/exiting the context, the lifespan manager executes the `startup/shutdown` event.
    # Startup events include 1. creating an engine, 2. creating session factory, and 3. initializing database tables.
    # Shutdown events include closing the engine.
    async with LifespanManager(app) as manager:
        yield manager
