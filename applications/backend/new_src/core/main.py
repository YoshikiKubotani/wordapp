from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from new_src.api.routers import decks, items, tests, users, login

from .config import settings


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
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
