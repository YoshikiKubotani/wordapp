from pydantic import AliasChoices, BaseModel, Field


class Deck(BaseModel):
    deck_id: int | None = None
    user_id: int
    deck_name: str

    @property
    def self_id(self) -> int | None:
        return self.deck_id