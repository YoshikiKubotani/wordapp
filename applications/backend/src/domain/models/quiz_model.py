from pydantic import BaseModel, PastDatetime, Field, AliasChoices


class Test(BaseModel):
    test_id: int | None = Field(default=None, validation_alias=AliasChoices("test_id", "self_id"))
    user_id: int
    deck_id: int
    test_type: str
    test_timestamp: PastDatetime


class TestItem(BaseModel):
    test_item_id: int | None = Field(default=None, validation_alias=AliasChoices("test_item_id", "self_id"))
    test_id: int
    item_id: int
    question_number: int
    choice_item_ids: list[int]
    correct_answer: int
    user_answer: int
    answer_time: int
