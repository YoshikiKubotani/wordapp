from pydantic import BaseModel, PastDatetime


class Test(BaseModel):
    self_id: int
    user_id: int
    deck_id: int
    test_type: str
    test_timestamp: PastDatetime


class TestItem(BaseModel):
    self_id: int
    test_id: int
    item_id: int
    question_number: int
    choice_item_ids: list[int]
    correct_answer: int
    user_answer: int
    answer_time: int
