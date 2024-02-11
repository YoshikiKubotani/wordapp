from collections.abc import AsyncIterator
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from src.core.config import settings
from src.core.main import app
from src.db.sqlalchemy_data_models import Base

from tests.src.utils import random_email, create_random_test_user, create_test_superuser

server_url = f"http://localhost:8000{settings.API_V1_STR}/"

settings.POSTGRES_SCHEMA = "test"
settings.TEST_USER_EMAIL = random_email()

@pytest.fixture(scope="session")
def anyio_backend() -> None:
    """Use the asyncio backend for asynchronous testing. This is necessary to avoid processing all the tests twice."""
    return "asyncio"


@pytest.fixture(scope="session")
async def lifespan_manager() -> AsyncIterator[LifespanManager]:
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


@pytest.fixture(scope="class")
async def async_test_client(lifespan_manager) -> AsyncClient:
    """Create an asynchronous test client.

    Yields:
        AsyncClient: An asynchronous test client.
    """
    async with AsyncClient(app=lifespan_manager.app, base_url=server_url) as async_client:
        yield async_client


@pytest.fixture(scope="class")
async def normal_async_test_client(async_test_client) -> AsyncIterator[AsyncClient]:
    """Create a normal asynchronous test client with table startup/cleanup events.

    Each test must be independent, necessitating the initialization of database tables for every test.
    Although the database is initialized within the lifespan event called by the lifespan manager
    at the startup of the FastAPI application, this is achieved through a session-scoped fixture,
    requiring redefinition at the function scope as well. The reason the lifespan event must also be used
    in tests is that the AsyncSessionFactory created within the lifespan event is utilized in the test target
    FastAPI endpoints through dependency injection.

    Yields:
        AsyncClient: An asynchronous test client which is authorized as a normal user.
    """
    # Import `engine` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import AsyncSessionFactory, engine

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with AsyncSessionFactory() as async_session:
        # Create a normal user for testing if it does not exist.
        normal_test_user = await create_random_test_user(async_session, settings.TEST_USER_EMAIL)

    # Log in as the normal user.
    response = await async_test_client.post(
        "/login/access-token",
        data={"username": normal_test_user.user_name, "password": normal_test_user.password},
    )

    token = response.json()["access_token"]
    token_type = response.json()["token_type"]
    async_test_client.headers = {"Authorization": f"{token_type} {token}"}

    # Yield the test client.
    yield async_test_client

    # Drop all tables defined as data models under `src/db` after the test is done.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def admin_async_test_client(async_test_client) -> AsyncIterator[AsyncClient]:
    """Create an admin asynchronous test client with table startup/cleanup events.

    Each test must be independent, necessitating the initialization of database tables for every test.
    Although the database is initialized within the lifespan event called by the lifespan manager
    at the startup of the FastAPI application, this is achieved through a session-scoped fixture,
    requiring redefinition at the function scope as well. The reason the lifespan event must also be used
    in tests is that the AsyncSessionFactory created within the lifespan event is utilized in the test target
    FastAPI endpoints through dependency injection.

    Yields:
        AsyncClient: An asynchronous test client which is authorized as a superuser.
    """
    # Import `engine` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import AsyncSessionFactory, engine

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with AsyncSessionFactory() as async_session:
        # Create the first superuser if it does not exist.
        await create_test_superuser(async_session)

    # Log in as the admin user.
    response = await async_test_client.post(
        "/login/access-token",
        data={"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD},
    )
    token = response.json()["access_token"]
    token_type = response.json()["token_type"]
    async_test_client.headers = {"Authorization": f"{token_type} {token}"}

    # Yield the test client.
    yield async_test_client

    # Drop all tables defined as data models under `src/db` after the test is done.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db_session(lifespan_manager: LifespanManager) -> AsyncIterator[AsyncSession]:
    """Provide an asynchronous database session.

    This fixture is used for testing which does not require an asynchronous test client.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    # Import `AsyncSessionFactory` and `engine` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import AsyncSessionFactory, engine

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with AsyncSessionFactory() as async_session:
        yield async_session

    # Drop all tables defined as data models under `src/db` after the test is done.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)