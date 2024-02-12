from pydantic import BaseModel, PastDatetime, Field, AliasChoices


class Item(BaseModel):
    item_id: int | None = Field(default=None, validation_alias=AliasChoices("item_id", "self_id"))
    user_id: int
    english: str
    japanese: str
    grade: int
    created_at: PastDatetime
    updated_at: PastDatetime
