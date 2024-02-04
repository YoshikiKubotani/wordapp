from pydantic import BaseModel


class CreateDeckRequest(BaseModel):
    deck_name: str


class DeckResponse(BaseModel):
    deck_id: int
    deck_name: str

class DeckSchema(BaseModel):
    _id: int
    user_id: int
    deck_name: str