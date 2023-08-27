from pydantic import BaseModel, Field

class TestItemDTO(BaseModel):
    item_id: int = Field(description="アイテムのID")
    item_index: int = Field(description="何問目の問題か")
    english: str = Field(description="単語の英語表記")
    op1: str = Field(description="１つ目の選択肢")
    op2: str = Field(description="２つ目の選択肢")
    op3: str = Field(description="３つ目の選択肢")
    op4: str = Field(description="４つ目の選択肢")
    answer: str = Field(description="正解の選択肢の内容")


class TestItemQuestionDTO(BaseModel):
    item_index: int = Field(description="何問目の問題か")
    english: str = Field(description="単語の英語表記")
    op1: str = Field(description="１つ目の選択肢")
    op2: str = Field(description="２つ目の選択肢")
    op3: str = Field(description="３つ目の選択肢")
    op4: str = Field(description="４つ目の選択肢")

class TestItemAnswerDTO(BaseModel):
    answer: str = Field(description="正解の選択肢の内容")