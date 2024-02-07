import datetime

from pydantic import BaseModel, PastDatetime


class TestItemAfterAttemptRequest(BaseModel):
    question_number: int
    choices: list[str]
    user_answer: int
    answer_time: int


class TestItemBeforeAttemptResponse(BaseModel):
    question_number: int
    choices: list[str]


class TestItemCheckedResponse(BaseModel):
    question_number: int
    choices: list[str]
    user_answer: int
    correct_answer: int
    answer_time: int


class TestMetaDataResponse(BaseModel):
    test_id: int
    timestamp: PastDatetime


class TestUnsolvedResponse(TestMetaDataResponse):
    test_items: list[TestItemBeforeAttemptResponse]


class TestCheckedResponse(TestMetaDataResponse):
    test_items: list[TestItemCheckedResponse]


class TestSchema(BaseModel):
    _id: int
    user_id: int
    deck_id: int
    test_type: str
    test_timestamp: PastDatetime


class TestItemSchema(BaseModel):
    _id: int
    test_id: int
    item_id: int
    question_number: int
    choice_item_ids: list[int]
    correct_answer: int
    user_answer: int
    answer_time: int
