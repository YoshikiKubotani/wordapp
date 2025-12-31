# ruff: noqa: B008, D417
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from starlette import status

from src.api.schemas import HealthCheckResponse, Word, WordCreate

router: APIRouter = APIRouter()

WORDS_FILE_PATH: Path = Path(__file__).resolve().parents[2] / "data" / "words.json"


def _load_words(storage_path: Path = WORDS_FILE_PATH) -> list[Word]:
    """Load stored words from disk.

    Args:
        storage_path (Path): The JSON file path where words are stored.

    Returns:
        list[Word]: The collection of stored words.

    Raises:
        HTTPException: Raised when the stored data cannot be parsed.
    """
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    if not storage_path.exists():
        return []

    content: str = storage_path.read_text(encoding="utf-8")
    if not content.strip():
        return []

    try:
        payload: list[dict[str, Any]] = json.loads(content)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse stored words.",
        ) from exc

    words: list[Word] = [Word.model_validate(item) for item in payload]
    return words


def _save_words(words: list[Word], storage_path: Path = WORDS_FILE_PATH) -> None:
    """Persist word entries to disk.

    Args:
        words (list[Word]): The word entries to persist.
        storage_path (Path): The JSON file path where words are stored.
    """
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    serialized_words: list[dict[str, Any]] = [
        word.model_dump(mode="json", by_alias=True) for word in words
    ]
    json_content: str = json.dumps(serialized_words, ensure_ascii=False, indent=2)
    storage_path.write_text(json_content, encoding="utf-8")


def _current_timestamp() -> datetime:
    """Generate a timezone-aware timestamp.

    Returns:
        datetime: The current UTC timestamp.
    """
    current_time: datetime = datetime.now(timezone.utc)
    return current_time


def _find_word_index(word_id: str, words: list[Word]) -> int:
    """Locate the index of a word by its identifier.

    Args:
        word_id (str): The identifier to search for.
        words (list[Word]): The collection to search through.

    Returns:
        int: The index of the matching word, or -1 if not found.
    """
    for index, word in enumerate(words):
        if word.id == word_id:
            return index
    return -1


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint.

    Returns:
        HealthCheckResponse: The status of the health check.
    """
    response: HealthCheckResponse = HealthCheckResponse(status="ok")
    return response


@router.get("/words", response_model=list[Word])
async def list_words() -> list[Word]:
    """Retrieve all stored words.

    Returns:
        list[Word]: The stored words.
    """
    words: list[Word] = _load_words()
    return words


@router.post("/words", response_model=Word, status_code=status.HTTP_201_CREATED)
async def create_word(payload: WordCreate) -> Word:
    """Create a new word entry.

    Args:
        payload (WordCreate): The word payload to persist.

    Returns:
        Word: The created word entry.
    """
    existing_words: list[Word] = _load_words()
    created_word: Word = Word(
        id=str(uuid4()),
        term=payload.term,
        meaning=payload.meaning,
        note=payload.note,
        created_at=_current_timestamp(),
    )
    updated_words: list[Word] = [*existing_words, created_word]
    _save_words(updated_words)
    return created_word


@router.put("/words/{word_id}", response_model=Word)
async def update_word(word_id: str, payload: WordCreate) -> Word:
    """Update an existing word entry.

    Args:
        word_id (str): The identifier of the word to update.
        payload (WordCreate): The new word values.

    Returns:
        Word: The updated word entry.

    Raises:
        HTTPException: If the word is not found.
    """
    existing_words: list[Word] = _load_words()
    target_index: int = _find_word_index(word_id, existing_words)
    if target_index == -1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found.",
        )

    existing_word: Word = existing_words[target_index]
    updated_word: Word = Word(
        id=existing_word.id,
        term=payload.term,
        meaning=payload.meaning,
        note=payload.note,
        created_at=existing_word.created_at,
    )
    existing_words[target_index] = updated_word
    _save_words(existing_words)
    return updated_word


@router.delete("/words/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(word_id: str) -> Response:
    """Delete a stored word.

    Args:
        word_id (str): The identifier of the word to delete.

    Returns:
        Response: An empty response indicating the deletion was successful.

    Raises:
        HTTPException: If the word is not found.
    """
    existing_words: list[Word] = _load_words()
    remaining_words: list[Word] = [
        word for word in existing_words if word.id != word_id
    ]
    if len(remaining_words) == len(existing_words):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found.",
        )

    _save_words(remaining_words)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
