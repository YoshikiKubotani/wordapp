from pydantic import BaseModel, PastDatetime


class QuizItemAfterAttemptRequest(BaseModel):
    question_number: int
    choices: list[str]
    user_answer: int
    answer_time: int


class QuizItemBeforeAttemptResponse(BaseModel):
    question_number: int
    choices: list[str]


class QuizItemCheckedResponse(BaseModel):
    question_number: int
    choices: list[str]
    user_answer: int
    correct_answer: int
    answer_time: int


class QuizMetaDataResponse(BaseModel):
    quiz_id: int
    timestamp: PastDatetime


class QuizUnsolvedResponse(QuizMetaDataResponse):
    quiz_items: list[QuizItemBeforeAttemptResponse]


class QuizCheckedResponse(QuizMetaDataResponse):
    quiz_items: list[QuizItemCheckedResponse]
