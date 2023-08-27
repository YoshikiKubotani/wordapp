from typing import Final, Any
from pydantic import UUID4

import fastapi
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from psycopg2.extensions import connection

from src.adapter.controller import TestController
from src.frameworks import get_db
from src.frameworks.postgres import ItemTable
from src.domain.dto import TestItemQuestionDTO, TestItemAnswerDTO

router: Final = fastapi.APIRouter(default_response_class=ORJSONResponse)


# ヘルスチェック
# @router.get("/health", response_model=Health)
# async def health() -> dict[str, str]:
#     """Endpoint for health check."""
#     return {"health": "ok"}

# テストセットの作成とそのUUIDの取得
@router.get("/tests/{grade_id}")
def make_test_set(grade_id: int, num: int) -> list[UUID4]:
    with get_db() as conn:
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
def get_question(item_uuid: UUID4) -> TestItemQuestionDTO:
    with get_db() as conn:
        item = TestController(
            # user_repository,
            ItemTable(conn),
            # genra_repository,
            # deck_repository,
            # score_repository,
            # history_repository,
        ).get_question(item_uuid)
    return item

# 与えられたUUIDを元に、問題の正解を取得
@router.get("/items/{item_uuid}/answer")
def get_answer(item_uuid: UUID4) -> TestItemAnswerDTO:
    with get_db() as conn:
        answer = TestController(
            # user_repository,
            ItemTable(conn),
            # genra_repository,
            # deck_repository,
            # score_repository,
            # history_repository,
        ).get_answer(item_uuid)
    return answer

# 与えられたUUIDの問題に対するユーザーの回答を受け取り、正誤判定を行う
@router.post("/items/{item_uuid}/response")
def check_answer(item_uuid: UUID4, response_info: dict[str, Any]) -> bool:
    with get_db() as conn:
        is_correct = TestController(
            # user_repository,
            ItemTable(conn),
            # genra_repository,
            # deck_repository,
            # score_repository,
            # history_repository,
        ).check_answer(item_uuid, response_info)
    return is_correct





