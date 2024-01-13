from pydantic import BaseModel


class DeckOut(BaseModel):
    deck_id: int
    deck_name: str

