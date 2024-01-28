import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from new_src.api.dependencies import CurrentUserDep, AsyncSessionDep
from new_src.api.schemas import (
    TestCheckedResponse,
    TestItemAfterAttemptRequest,
    TestItemBeforeAttemptResponse,
    TestItemCheckedResponse,
    TestMetaDataResponse,
    TestUnsolvedResponse,
)

router = APIRouter()


@router.get("/", response_model=list[TestMetaDataResponse])
async def read_all_tests(
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Read all the tests attempted by a user."""
    tests = [
        TestMetaDataResponse(
            test_id=1,
            timestamp=datetime.datetime.now(),
        )
    ]
    return tests


@router.post("/", response_model=TestUnsolvedResponse)
async def create_test(
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Create a new test."""
    return TestUnsolvedResponse(
        test_id=1,
        test_items=[
            TestItemBeforeAttemptResponse(
                question_number=1,
                choices=[
                    "dummy_choice_1",
                    "dummy_choice_2",
                    "dummy_choice_3",
                    "dummy_choice_4",
                ],
            ),
            TestItemBeforeAttemptResponse(
                question_number=2,
                choices=[
                    "dummy_choice_1",
                    "dummy_choice_2",
                    "dummy_choice_3",
                    "dummy_choice_4",
                ],
            ),
        ],
        timestamp=datetime.datetime.now(),
    )


@router.post("/{test_id}", response_model=TestCheckedResponse)
async def answer_test(
    test_id: int,
    # solved_items: list[TestItemAfterAttemptRequest],
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Answer a test."""
    return TestCheckedResponse(
        test_id=test_id,
        test_items=[
            TestItemCheckedResponse(
                question_number=1,
                choices=[
                    "dummy_choice_1",
                    "dummy_choice_2",
                    "dummy_choice_3",
                    "dummy_choice_4",
                ],
                user_answer=1,
                correct_answer=1,
                answer_time=1000,
            ),
            TestItemCheckedResponse(
                question_number=2,
                choices=[
                    "dummy_choice_1",
                    "dummy_choice_2",
                    "dummy_choice_3",
                    "dummy_choice_4",
                ],
                user_answer=1,
                correct_answer=1,
                answer_time=1000,
            ),
        ],
        timestamp=datetime.datetime.now(),
    )


@router.get("/{test_id}/items", response_model=list[TestItemCheckedResponse])
async def read_test_items(
    test_id: int,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Get all the items in a test."""
    return [
        TestItemCheckedResponse(
            question_number=1,
            choices=[
                "dummy_choice_1",
                "dummy_choice_2",
                "dummy_choice_3",
                "dummy_choice_4",
            ],
            user_answer=1,
            correct_answer=1,
            answer_time=1000,
        ),
        TestItemCheckedResponse(
            question_number=2,
            choices=[
                "dummy_choice_1",
                "dummy_choice_2",
                "dummy_choice_3",
                "dummy_choice_4",
            ],
            user_answer=1,
            correct_answer=1,
            answer_time=1000,
        ),
    ]
