from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Any
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from pydantic import ValidationError

from src.api.schemas import Word, WordCreate

TABLE_NAME_ENV_VAR: str = "WORDS_TABLE_NAME"
BASE_HEADERS: dict[str, str] = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}


def _response(
    body: dict[str, Any] | list[dict[str, Any]] | None,
    status_code: HTTPStatus,
) -> dict[str, Any]:
    """Build a standard API Gateway response.

    Args:
        body (dict[str, Any] | list[dict[str, Any]] | None): The response payload.
        status_code (HTTPStatus): The HTTP status code to return.

    Returns:
        dict[str, Any]: The formatted API Gateway response.
    """
    payload: dict[str, Any] | list[dict[str, Any]] = body or {}
    serialized_body: str = json.dumps(payload, ensure_ascii=False)
    response: dict[str, Any] = {
        "statusCode": int(status_code),
        "headers": {**BASE_HEADERS},
        "body": serialized_body,
    }
    return response


def _error_response(status_code: HTTPStatus, message: str) -> dict[str, Any]:
    """Create an error response with a message.

    Args:
        status_code (HTTPStatus): The HTTP status code to return.
        message (str): The error message to include.

    Returns:
        dict[str, Any]: The formatted error response.
    """
    error_body: dict[str, str] = {"message": message}
    return _response(error_body, status_code)


def _parse_body(event: dict[str, Any]) -> dict[str, Any]:
    """Parse the JSON body from the API Gateway event.

    Args:
        event (dict[str, Any]): The API Gateway event payload.

    Returns:
        dict[str, Any]: The parsed JSON body, or an empty dictionary if not provided.

    Raises:
        ValueError: If the body cannot be parsed as JSON.
    """
    raw_body: str | None = event.get("body")
    if raw_body is None:
        return {}

    try:
        body: dict[str, Any] = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON body.") from exc

    return body


def _extract_word_id(path: str) -> tuple[bool, str | None]:
    """Identify whether the request targets the words resource and extract the identifier.

    Args:
        path (str): The request path.

    Returns:
        tuple[bool, str | None]: A tuple indicating whether the path is under /words
        and the extracted identifier when present.
    """
    segments: list[str] = [segment for segment in path.split("/") if segment]
    if "words" not in segments:
        return False, None

    words_index: int = segments.index("words")
    has_identifier: bool = words_index + 1 < len(segments)
    word_id: str | None = segments[words_index + 1] if has_identifier else None
    return True, word_id


def _get_table() -> Any:
    """Instantiate the DynamoDB table resource using the configured table name.

    Returns:
        Any: The DynamoDB table resource.

    Raises:
        RuntimeError: If the environment variable is missing.
    """
    table_name: str | None = os.getenv(TABLE_NAME_ENV_VAR)
    if not table_name:
        raise RuntimeError("WORDS_TABLE_NAME environment variable is not set.")

    dynamodb_resource: Any = boto3.resource("dynamodb")
    table: Any = dynamodb_resource.Table(table_name)
    return table


def _serialize_word(word: Word) -> dict[str, Any]:
    """Serialize a Word model into a JSON-ready dictionary.

    Args:
        word (Word): The word model instance.

    Returns:
        dict[str, Any]: A dictionary representation suitable for JSON responses.
    """
    serialized: dict[str, Any] = word.model_dump(mode="json", by_alias=True)
    return serialized


def _list_words(table: Any) -> dict[str, Any]:
    """List all words stored in DynamoDB.

    Args:
        table (Any): The DynamoDB table resource.

    Returns:
        dict[str, Any]: The HTTP response with all stored words.
    """
    try:
        scan_result: dict[str, Any] = table.scan()
    except ClientError as exc:
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    items: list[dict[str, Any]] = scan_result.get("Items", [])
    words: list[Word] = [Word.model_validate(item) for item in items]
    serialized_words: list[dict[str, Any]] = [
        _serialize_word(word) for word in words
    ]
    return _response(serialized_words, HTTPStatus.OK)


def _create_word(table: Any, event: dict[str, Any]) -> dict[str, Any]:
    """Create a new word and persist it to DynamoDB.

    Args:
        table (Any): The DynamoDB table resource.
        event (dict[str, Any]): The API Gateway event payload.

    Returns:
        dict[str, Any]: The HTTP response containing the created word.
    """
    try:
        payload_dict: dict[str, Any] = _parse_body(event)
        payload: WordCreate = WordCreate.model_validate(payload_dict)
    except (ValidationError, ValueError) as exc:
        return _error_response(HTTPStatus.BAD_REQUEST, str(exc))

    created_at: str = datetime.now(timezone.utc).isoformat()
    item: dict[str, Any] = {
        "id": str(uuid4()),
        "term": payload.term,
        "meaning": payload.meaning,
        "createdAt": created_at,
    }
    if payload.note is not None:
        item["note"] = payload.note

    try:
        table.put_item(Item=item)
    except ClientError as exc:
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    word: Word = Word.model_validate(item)
    serialized_word: dict[str, Any] = _serialize_word(word)
    return _response(serialized_word, HTTPStatus.CREATED)


def _update_word(table: Any, word_id: str, event: dict[str, Any]) -> dict[str, Any]:
    """Update an existing word entry in DynamoDB.

    Args:
        table (Any): The DynamoDB table resource.
        word_id (str): The identifier of the word to update.
        event (dict[str, Any]): The API Gateway event payload.

    Returns:
        dict[str, Any]: The HTTP response containing the updated word.
    """
    try:
        payload_dict: dict[str, Any] = _parse_body(event)
        payload: WordCreate = WordCreate.model_validate(payload_dict)
    except (ValidationError, ValueError) as exc:
        return _error_response(HTTPStatus.BAD_REQUEST, str(exc))

    try:
        existing_item_response: dict[str, Any] = table.get_item(Key={"id": word_id})
    except ClientError as exc:
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    existing_item: dict[str, Any] | None = existing_item_response.get("Item")
    if existing_item is None:
        return _error_response(HTTPStatus.NOT_FOUND, "Word not found.")

    existing_item["term"] = payload.term
    existing_item["meaning"] = payload.meaning
    if payload.note is None:
        existing_item.pop("note", None)
    else:
        existing_item["note"] = payload.note

    try:
        table.put_item(Item=existing_item)
    except ClientError as exc:
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    word: Word = Word.model_validate(existing_item)
    serialized_word: dict[str, Any] = _serialize_word(word)
    return _response(serialized_word, HTTPStatus.OK)


def _delete_word(table: Any, word_id: str) -> dict[str, Any]:
    """Delete a word from DynamoDB.

    Args:
        table (Any): The DynamoDB table resource.
        word_id (str): The identifier of the word to delete.

    Returns:
        dict[str, Any]: An empty HTTP response indicating success.
    """
    try:
        delete_result: dict[str, Any] = table.delete_item(
            Key={"id": word_id},
            ReturnValues="ALL_OLD",
        )
    except ClientError as exc:
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    deleted_item: dict[str, Any] | None = delete_result.get("Attributes")
    if deleted_item is None:
        return _error_response(HTTPStatus.NOT_FOUND, "Word not found.")

    return _response({}, HTTPStatus.NO_CONTENT)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Entry point for the Lambda function handling word CRUD operations.

    Args:
        event (dict[str, Any]): The API Gateway request event.
        context (Any): Lambda execution context (unused).

    Returns:
        dict[str, Any]: The HTTP response for API Gateway.
    """
    path: str = event.get("path", "")
    http_method: str = event.get("httpMethod", "").upper()
    is_word_route: bool
    word_id: str | None
    is_word_route, word_id = _extract_word_id(path)

    if not is_word_route:
        return _error_response(HTTPStatus.NOT_FOUND, "Route not found.")

    try:
        table: Any = _get_table()
    except RuntimeError as exc:
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    if http_method == "GET" and word_id is None:
        return _list_words(table)

    if http_method == "POST" and word_id is None:
        return _create_word(table, event)

    if http_method == "PUT" and word_id is not None:
        return _update_word(table, word_id, event)

    if http_method == "DELETE" and word_id is not None:
        return _delete_word(table, word_id)

    return _error_response(HTTPStatus.METHOD_NOT_ALLOWED, "Unsupported method for this route.")
