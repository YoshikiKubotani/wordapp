from collections.abc import Sequence
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.settings import settings

app = FastAPI(
    debug=True,
)

# Set all CORS enabled origins.
if settings.CORS_ALLOW_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix="/api")


@app.exception_handler(HTTPException)
async def handle_http_exception(_request: Request, exc: HTTPException) -> JSONResponse:
    """Convert HTTP exceptions into JSON responses with a message field.

    Args:
        _request (Request): The incoming FastAPI request (unused).
        exc (HTTPException): The HTTP exception to serialize.

    Returns:
        JSONResponse: JSON response carrying the error message.
    """
    message: str = exc.detail if isinstance(exc.detail, str) else "Request failed."
    response: JSONResponse = JSONResponse(
        status_code=exc.status_code,
        content={"message": message},
    )
    return response


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return a user-friendly validation error response.

    Args:
        _request (Request): The incoming FastAPI request (unused).
        exc (RequestValidationError): The validation error raised by FastAPI.

    Returns:
        JSONResponse: JSON response carrying the validation error message.
    """
    error_details: Sequence[dict[str, Any]] = exc.errors()
    first_error: dict[str, Any] = error_details[0] if error_details else {}
    error_message: str = first_error.get("msg", "Invalid request payload.")
    response: JSONResponse = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": error_message},
    )
    return response
