from pydantic import BaseModel


class Deck(BaseModel):
    self_id: int
    user_id: int
    deck_name: str
