from pathlib import Path
from typing import Final, Optional, Any
from pydantic import UUID4

import fastapi
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from psycopg2.extensions import connection

from src.adapter.controller import TestController
from src.frameworks import get_db
from src.frameworks.postgres import ItemTable

router: Final = fastapi.APIRouter(default_response_class=ORJSONResponse)


# ヘルスチェック
# @router.get("/health", response_model=Health)
# async def health() -> dict[str, str]:
#     """Endpoint for health check."""
#     return {"health": "ok"}

# テストセットの作成とそのUUIDの取得
@router.get("/tests/{grade_id}")
def make_test_set(grade_id: int, num: int, conn: connection = Depends(get_db)) -> list[UUID4]:
    with conn as conn:
        test_set = TestController(
            # user_repository,
            ItemTable(conn),
            # genra_repository,
            # deck_repository,
            # score_repository,
            # history_repository,
        ).make_test_set(grade_id, num)
    return test_set

# 与えられたUUIDを元に、キャッシュされたテストセットの中の問題を取得
@router.get("/items/{item_uuid}")
def get_item(item_uuid: UUID4) -> dict[str, Any]:
    return {
        "item_index": 1,
        "english": "Hello",
        "op1": "こんにちは",
        "op2": "こんばんは",
        "op3": "おはよう",
        "op4": "さようなら",
    }

# 与えられたUUIDを元に、問題の正解を取得
@router.get("/items/{item_uuid}/answer")
def get_answer(item_uuid: UUID4) -> dict[str, str]:
    return {"answer": "こんにちは"}

# 与えられたUUIDの問題に対するユーザーの回答を受け取る
@router.post("/items/{item_uuid}/response")
def post_response(item_uuid: UUID4, answer_info: dict[str, str]) -> bool:
    print(answer_info)
    return True

# # 新規エージェントの登録
# @router.post("/agents")
# async def register_agent(
#     register_agent_dto: RegisterAgentDTO, connection: connection = Depends(get_db)
# ) -> AgentDTO:
#     return AgentController(function_calling_handler, connection).create_agent(
#         register_agent_dto
#     )

