from pydantic import BaseModel


class ItemOut(BaseModel):
    item_id: int
    english: str
    japanese: str
    grade: int