from pydantic import Field
from pydantic.dataclasses import dataclass

from src.domain import EntityConfig


@dataclass(config=EntityConfig)
class ItemEntity:
    item_id: int = Field(description="アイテムのID")
    english: str = Field(description="単語の英語表記")
    japanese: str = Field(description="単語の日本語訳")
    grade: int = Field(description="単語のレベル")
