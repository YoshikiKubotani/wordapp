from pydantic import BaseModel, PastDatetime

class CreateItemRequest(BaseModel):
    english: str
    japanese: str
    grade: int


class UpdateItemRequest(BaseModel):
    english: str
    japanese: str
    grade: int


class ItemResponse(BaseModel):
    item_id: int
    english: str
    japanese: str
    grade: int

class ItemSchema(BaseModel):
    _id: int
    user_id: int
    english: str
    japanese: str
    grade: int
    created_at: PastDatetime
    updated_at: PastDatetime