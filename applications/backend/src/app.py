from contextlib import asynccontextmanager
import inspect
from typing import Final, AsyncIterator

import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import routers
from src.utils import get_my_logger, initialize_all
from src.frameworks import PostgreSQL, postgres, get_db

logger = get_my_logger(__name__)

def main() -> fastapi.FastAPI:
    """Create FastAPI application instance.

    Returns:
        fastapi.FastAPI: A FastAPI application instance.

    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator:
        # Startup
        logger.info("Starup...")
        # PostgresSQLのテーブルを管理するクラスの一覧を取得
        all_tool_classes = [
            cls[1](conn) for cls in inspect.getmembers(postgres, inspect.isclass)
        ]
        # テストの際はここでtestスキーマにあるテーブルを削除・再作成する
        with get_db() as conn:
            PostgreSQL.recreate_schema(conn)

        # テーブルを作成
        initialize_all(all_tool_classes)
        yield
        # Cleanup(shutdown)
        logger.info("Shutdown...")

    app: Final = fastapi.FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routers.router)
    return app