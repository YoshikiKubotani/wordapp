# ruff: noqa: D101
from pydantic import BaseModel


class CreateDeckRequest(BaseModel):
    deck_name: str


class DeckResponse(BaseModel):
    deck_id: int
    deck_name: str
