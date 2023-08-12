import uuid
from pathlib import Path
from typing import Final, Optional, Any
from pydantic import UUID4

import fastapi
from fastapi import Depends
from fastapi.responses import ORJSONResponse


router: Final = fastapi.APIRouter(default_response_class=ORJSONResponse)


# ヘルスチェック
# @router.get("/health", response_model=Health)
# async def health() -> dict[str, str]:
#     """Endpoint for health check."""
#     return {"health": "ok"}

# テストセットの作成とそのUUIDの取得
@router.get("/tests/{grade_id}")
def make_test_set(grade_id: int) -> list[UUID4]:
    testset_list = []
    for i in range(10):
        testset_list.append(uuid.uuid4())
    print(testset_list)
    return testset_list

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

# # 新規エージェントの登録
# @router.post("/agents")
# async def register_agent(
#     register_agent_dto: RegisterAgentDTO, connection: connection = Depends(get_db)
# ) -> AgentDTO:
#     return AgentController(function_calling_handler, connection).create_agent(
#         register_agent_dto
#     )

