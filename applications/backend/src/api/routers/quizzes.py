import datetime
from typing import Any

from fastapi import APIRouter

from src.api.dependencies import async_session_dependency, current_user_dependency
from src.api.schemas import (
    QuizCheckedResponse,
    QuizItemAfterAttemptRequest,
    QuizItemBeforeAttemptResponse,
    QuizItemCheckedResponse,
    QuizMetaDataResponse,
    QuizUnsolvedResponse,
)

router = APIRouter()


@router.get("/", response_model=list[QuizMetaDataResponse])
async def read_all_quizzes(
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Read all the quizzes attempted by a user.

    Args:
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        list[QuizMetaDataResponse]: The list of all quizzes.
    """
    quizzes = [
        QuizMetaDataResponse(
            quiz_id=1,
            timestamp=datetime.datetime.now(),
        )
    ]
    return quizzes


@router.post("/", response_model=QuizUnsolvedResponse)
async def create_quiz(
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Create a new quiz.

    Args:
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        QuizUnsolvedResponse: The created quiz.
    """
    return QuizUnsolvedResponse(
        quiz_id=1,
        quiz_items=[
            QuizItemBeforeAttemptResponse(
                question_number=1,
                choices=[
                    "dummy_choice_1",
                    "dummy_choice_2",
                    "dummy_choice_3",
                    "dummy_choice_4",
                ],
            ),
            QuizItemBeforeAttemptResponse(
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


@router.post("/{quiz_id}", response_model=QuizCheckedResponse)
async def answer_quiz(
    quiz_id: int,
    solved_items: list[QuizItemAfterAttemptRequest],
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Answer a quiz.

    Args:
        quiz_id (int): The quiz id.
        solved_items (list[QuizItemAfterAttemptRequest]): The list of solved items.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        QuizCheckedResponse: The checked quiz.
    """
    return QuizCheckedResponse(
        quiz_id=quiz_id,
        quiz_items=[
            QuizItemCheckedResponse(
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
            QuizItemCheckedResponse(
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


@router.get("/{quiz_id}/items", response_model=list[QuizItemCheckedResponse])
async def read_quiz_items(
    quiz_id: int,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Get all the items in a quiz.

    Args:
        quiz_id (int): The quiz id.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        list[QuizItemCheckedResponse]: The list of quiz items.
    """
    return [
        QuizItemCheckedResponse(
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
        QuizItemCheckedResponse(
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
