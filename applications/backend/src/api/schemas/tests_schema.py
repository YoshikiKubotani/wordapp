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


