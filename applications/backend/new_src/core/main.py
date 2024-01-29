from typing import cast
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from collections.abc import AsyncIterator

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from new_src.api.routers import decks, items, login, tests, users

from .config import settings


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

AsyncSessionFactory: async_sessionmaker[AsyncSession] | None = None

# This is the lifespan context manager, which is called once before/after the server starts/stops.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global AsyncSessionFactory
    # Create a new async engine instance, which offers a session environment to manage a database.
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())
    # Create a factiry that returns a new AsyncSession instance.
    AsyncSessionFactory = cast(async_sessionmaker[AsyncSession], async_sessionmaker(engine, expire_on_commit=False))
    
    # Yield the app instance.
    yield
    
    # Close the engine instance as a clean-up operation.
    await engine.dispose()

app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(decks.router, prefix="/decks", tags=["decks"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

app.include_router(api_router, prefix=settings.API_V1_STR)
