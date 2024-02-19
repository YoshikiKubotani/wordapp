from pydantic import BaseModel, PastDatetime, Field, AliasChoices


class Quiz(BaseModel):
    quiz_id: int | None = Field(default=None, validation_alias=AliasChoices("quiz_id", "self_id"))
    user_id: int
    deck_id: int
    quiz_type: str
    quiz_timestamp: PastDatetime


class QuizItem(BaseModel):
    quiz_item_id: int | None = Field(default=None, validation_alias=AliasChoices("quiz_item_id", "self_id"))
    quiz_id: int
    item_id: int
    question_number: int
    choice_item_ids: list[int]
    correct_answer: int
    user_answer: int
    answer_time: int
