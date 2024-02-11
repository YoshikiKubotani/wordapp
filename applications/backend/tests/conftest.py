from collections.abc import AsyncIterator
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from src.core.config import settings
from src.core.main import app
from src.db.sqlalchemy_data_models import Base
from src.scripts.init_db import create_first_superuser

from tests.src.utils import random_email, create_random_test_user

server_url = f"http://localhost:8000{settings.API_V1_STR}/"

settings.POSTGRES_SCHEMA = "test"
settings.TEST_USER_EMAIL = random_email()

# def setup_class_attributes(target_cls: Any, config: dict[str, str]) -> set[str]:
#     found_attributes: set = set()
#     if hasattr(target_cls, "fixture_overridden_attribute_names"):
#         for attribute in target_cls.fixture_overridden_attribute_names:
#             if attribute in config:
#                 setattr(target_cls, attribute, config[attribute])
#                 found_attributes.add(attribute)
#     unfound_attributes = set(config.keys()) - found_attributes
#     return unfound_attributes

from starlette.datastructures import State
from typing import TypedDict

class Resource(TypedDict):
    """Define a resource type for the `resources` fixture."""
    async_client: AsyncClient
    app_state: State

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
async def resource(lifespan_manager) -> AsyncIterator[Resource]:
    """Create an asynchronous test client.

    Yields:
        AsyncClient: An asynchronous test client.
    """
    async with AsyncClient(app=lifespan_manager.app, base_url=server_url) as async_client:
        print(lifespan_manager.app)
        yield {"async_client": async_client, "app_state": lifespan_manager.app.state}


@pytest.fixture(scope="class")
async def normal_async_test_client(resource) -> AsyncIterator[AsyncClient]:
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
    engine = resource["app_state"].engine
    async_test_client = resource["async_client"]

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a normal user for testing if it does not exist.
    normal_test_user = await create_random_test_user(settings.TEST_USER_EMAIL, async_test_client)

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


# @pytest.fixture(scope="function")
# async def wrapped_normal_async_test_client(normal_async_test_client) -> AsyncIterator[AsyncClient]:
#     """Create an asynchronous test client with table startup/cleanup events.

#     Each test must be independent, necessitating the initialization of database tables for every test.
#     Although the database is initialized within the lifespan event called by the lifespan manager
#     at the startup of the FastAPI application, this is achieved through a session-scoped fixture,
#     requiring redefinition at the function scope as well. The reason the lifespan event must also be used
#     in tests is that the AsyncSessionFactory created within the lifespan event is utilized in the test target
#     FastAPI endpoints through dependency injection.

#     Yields:
#         AsyncClient: An asynchronous test client.
#     """
#     engine = normal_async_test_client.app.state.engine

#     # Create all tables defined as data models under `src/db` if they do not exist.
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     # Yield the test client.
#     yield normal_async_test_client

#     # Drop all tables defined as data models under `src/db` after the test is done.
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def admin_async_test_client(resource) -> AsyncIterator[AsyncClient]:
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
    engine = resource["app_state"].engine
    async_test_client = resource["async_client"]

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create the first superuser if it does not exist.
    await create_first_superuser(async_test_client)

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
    # Import `AsyncSessionFactory` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import AsyncSessionFactory

    engine = lifespan_manager.app.state.engine

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with AsyncSessionFactory() as async_session:
        yield async_session

    # Drop all tables defined as data models under `src/db` after the test is done.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




# @pytest.fixture(scope="class")
# async def authenticated_async_test_client(async_test_client):
#     """Create an authenticated user for testing."""
#     response = await async_test_client.post(
#         "/login/access-token",
#         data={"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD},
#     )
#     print("response", response.json())
#     token = response.json()["access_token"]
#     token_type = response.json()["token_type"]
#     async_test_client.headers = {"Authorization": f"{token_type} {token}"}
#     yield async_test_client


# @pytest.fixture(scope="class")
# async def assingn_authenticated_async_test_client_to_class(
#     request, authenticated_async_test_client
# ):
#     """Assign the authenticated client to the class.

#     This is used to override the client fixture in the test class.
#     """
#     unfound_attributes = setup_class_attributes(
#         request.cls, {"client": authenticated_async_test_client}
#     )
#     if "client" in unfound_attributes:
#         raise ValueError(
#             'The test class must have "fixture_overridden_attribute_names" attribute which contains "client" to assign authenticated async test client.'
#         )
#     yield
