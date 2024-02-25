from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field, PastDatetime


class Quiz(BaseModel):
    quiz_id: int | None = None
    user_id: int
    deck_id: int
    quiz_type: str
    quiz_timestamp: PastDatetime = datetime.now()

    @property
    def self_id(self) -> int | None:
        return self.quiz_id

class QuizItem(BaseModel):
    quiz_item_id: int | None = None
    quiz_id: int
    item_id: int
    question_number: int
    choice_item_ids: list[int]
    correct_answer: int
    user_answer: int | None = None
    answer_time: int | None = None

    @property
    def self_id(self) -> int | None:
        return self.quiz_item_id