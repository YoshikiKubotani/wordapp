import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from src.core.config import settings
from src.db.models.sqlalchemy_data_models import Base
from tests.utils import create_random_test_user, create_test_superuser

server_url = f"http://localhost:8000{settings.API_V1_STR}/"


@pytest.fixture(scope="class")
async def async_test_client(lifespan_manager: LifespanManager) -> AsyncClient:
    """Create an asynchronous test client.

    Yields:
        AsyncClient: An asynchronous test client.
    """
    async with AsyncClient(
        app=lifespan_manager.app, base_url=server_url  # type: ignore
    ) as async_client:
        yield async_client


@pytest.fixture(scope="class")
async def normal_async_test_client(async_test_client: AsyncClient) -> AsyncClient:
    """Create a normal asynchronous test client with table startup/cleanup events.

    Each test must be independent, necessitating the initialization of database tables for every test.
    Although the database is initialized within the lifespan event called by the lifespan manager
    at the startup of the FastAPI application, this is achieved through a session-scoped fixture,
    requiring redefinition at the function scope as well. The reason the lifespan event must also be used
    in tests is that the async_session_factory created within the lifespan event is utilized in the test target
    FastAPI endpoints through dependency injection.

    Returns:
        AsyncClient: An asynchronous test client which is authorized as a normal user.
    """
    # Import `engine` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import async_session_factory, engine

    # Drop and create all tables defined as data models under `src/db`.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with async_session_factory() as async_session:
        # Create a normal user for testing if it does not exist.
        request_form = await create_random_test_user(async_session)

    # Log in as the normal user.
    response = await async_test_client.post(
        "/login/access-token",
        data=request_form,
    )

    token = response.json()["access_token"]
    token_type = response.json()["token_type"]
    async_test_client.headers = {"Authorization": f"{token_type} {token}"}

    # Return the test client.
    return async_test_client


@pytest.fixture(scope="function")
async def admin_async_test_client(async_test_client: AsyncClient) -> AsyncClient:
    """Create an admin asynchronous test client with table startup/cleanup events.

    Each test must be independent, necessitating the initialization of database tables for every test.
    Although the database is initialized within the lifespan event called by the lifespan manager
    at the startup of the FastAPI application, this is achieved through a session-scoped fixture,
    requiring redefinition at the function scope as well. The reason the lifespan event must also be used
    in tests is that the async_session_factory created within the lifespan event is utilized in the test target
    FastAPI endpoints through dependency injection.

    Returns:
        AsyncClient: An asynchronous test client which is authorized as a superuser.
    """
    # Import `engine` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import async_session_factory, engine

    # Drop and create all tables defined as data models under `src/db`.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with async_session_factory() as async_session:
        # Create the first superuser if it does not exist.
        request_form = await create_test_superuser(async_session)

    # Log in as the admin user.
    response = await async_test_client.post(
        "/login/access-token",
        data=request_form,
    )
    token = response.json()["access_token"]
    token_type = response.json()["token_type"]
    async_test_client.headers = {"Authorization": f"{token_type} {token}"}

    # Return the test client.
    return async_test_client
