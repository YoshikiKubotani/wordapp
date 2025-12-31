from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HealthCheckResponse(BaseModel):
    """The response for the health check endpoint.

    Attributes:
        status (str): The status of the health check.
    """

    status: Annotated[str, Field(..., description="The status of the health check.")]


class WordBase(BaseModel):
    """Shared attributes for word payloads.

    Attributes:
        term (str): The vocabulary term to memorize.
        meaning (str): The meaning of the term.
        note (str | None): An optional hint to help remember the term.
    """

    term: Annotated[str, Field(..., description="The vocabulary term to memorize.")]
    meaning: Annotated[str, Field(..., description="The meaning of the term.")]
    note: Annotated[
        str | None,
        Field(None, description="An optional hint to help remember the term."),
    ]

    @field_validator("term", "meaning")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Ensure text fields are not empty or whitespace.

        Args:
            value (str): The raw input value.

        Returns:
            str: The trimmed value.

        Raises:
            ValueError: If the value is empty after trimming.
        """
        text: str = value.strip()
        if not text:
            raise ValueError("Value cannot be empty.")
        return text

    @field_validator("note")
    @classmethod
    def normalize_note(cls, value: str | None) -> str | None:
        """Normalize optional note fields by trimming whitespace.

        Args:
            value (str | None): The raw input value.

        Returns:
            str | None: The trimmed note or None if empty.
        """
        if value is None:
            return None
        note_text: str = value.strip()
        return note_text or None


class WordCreate(WordBase):
    """Payload used when creating or updating a word entry."""


class Word(WordBase):
    """A stored word entry.

    Attributes:
        id (str): A unique identifier for the word.
        created_at (datetime): The time the word was created.
    """

    id: Annotated[str, Field(..., description="A unique identifier for the word.")]
    created_at: Annotated[
        datetime,
        Field(
            ...,
            alias="createdAt",
            description="ISO timestamp when the word was created.",
        ),
    ]

    model_config = ConfigDict(populate_by_name=True)
