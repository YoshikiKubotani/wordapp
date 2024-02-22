import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from asgi_lifespan import LifespanManager

from src.db.models.sqlalchemy_data_models import Base


@pytest.fixture(scope="function")
async def async_db_session(
    lifespan_manager: LifespanManager,
) -> AsyncSession:
    """Provide an asynchronous database session.

    This fixture is used for testing which does not require an asynchronous test client.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    # Import `async_session_factory` and `engine` here to make sure the lifespan manager is executed before creating the session.
    from src.core.main import async_session_factory, engine

    # Drop and create all tables defined as data models under `src/db`.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with async_session_factory() as async_session:
        yield async_session
