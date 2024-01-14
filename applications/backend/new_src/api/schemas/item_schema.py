from pydantic import BaseModel

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
