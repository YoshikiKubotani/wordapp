from typing import Final

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from src import routers
from src.utils import get_my_logger

logger = get_my_logger(__name__)

def main() -> fastapi.FastAPI:
    """Create FastAPI application instance.

    Returns:
        fastapi.FastAPI: A FastAPI application instance.

    """
    app: Final = fastapi.FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routers.router)
    return app