from pydantic import BaseModel, PastDatetime


class Item(BaseModel):
    self_id: int
    user_id: int
    english: str
    japanese: str
    grade: int
    created_at: PastDatetime
    updated_at: PastDatetime
