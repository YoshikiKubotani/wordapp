import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from starlette.middleware.cors import CORSMiddleware

from src.api.routers import decks, items, login, quizzes, users
from src.db.models.sqlalchemy_data_models import Base

from .config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate a unique id for each route.

    Args:
        route (APIRoute): The route.

    Returns:
        str: The unique id.
    """
    return f"{route.tags[0]}-{route.name}"


async_session_factory: async_sessionmaker[AsyncSession] | None = None
engine: AsyncEngine | None = None


# This is the lifespan context manager, which is called once before/after the server starts/stops.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Run startup and shutdown events of the app.

    FastAPI lifespan events are used to run code before the app starts and after the app stops.
    More specifically, the code before `yield` is executed before the app starts, and the code
    after `yield` is executed after the app stops.

    Args:
        app (FastAPI): The FastAPI app instance.

    Yields:
        None: This function yields nothing
    """
    print("Running startup lifespan events ...")

    global engine
    global async_session_factory
    # Create a new async engine instance, which offers a session environment to manage a database.
    engine = create_async_engine(cast(str, settings.SQLALCHEMY_DATABASE_URI))
    # Create a factiry that returns a new AsyncSession instance.
    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

    # Create all tables defined as data models under `src/db` if they do not exist.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Yield nothing, but boot up the FastAPI app instance. If the app stops, the code after the yield will run.
    yield

    print("Running shutdown lifespan events ...")
    # Close the engine instance as a clean-up operation.
    await engine.dispose()


app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin for origin in json.loads(settings.BACKEND_CORS_ORIGINS)],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(decks.router, prefix="/decks", tags=["decks"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

app.include_router(api_router, prefix=settings.API_V1_STR)
