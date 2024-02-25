from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field, PastDatetime


class Item(BaseModel):
    item_id: int | None = None
    user_id: int
    english: str
    japanese: str
    grade: int
    created_at: PastDatetime = datetime.now()
    updated_at: PastDatetime = datetime.now()

    @property
    def self_id(self) -> int | None:
        return self.item_id
