from pydantic import BaseModel


class Deck(BaseModel):
    _id: int
    user_id: int
    deck_name: str
