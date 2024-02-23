from pydantic import AliasChoices, BaseModel, Field


class Deck(BaseModel):
    deck_id: int | None = Field(
        default=None, validation_alias=AliasChoices("deck_id", "self_id")
    )
    user_id: int
    deck_name: str
