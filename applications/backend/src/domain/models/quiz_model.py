from datetime import datetime

from pydantic import PastDatetime

from .base_model import BaseDomainModel


class Quiz(BaseDomainModel):
    """The domain model for a quiz.

    Attributes:
        quiz_id (int | None): The unique identifier for the quiz.
        user_id (int): The unique identifier for the user who solved the quiz.
        deck_id (int): The unique identifier for the deck that the quiz is based on.
        quiz_type (str): The type of the quiz.
        quiz_timestamp (PastDatetime): The date and time when the quiz was taken.
    """

    quiz_id: int | None = None
    user_id: int
    deck_id: int | None
    quiz_type: str
    quiz_timestamp: PastDatetime = datetime.now()

    @property
    def self_id(self) -> int | None:
        """The alias of unique identifier for the quiz.

        This property is required by the base repository, which is solely
        responsible for all CRUD operations.

        Returns:
            int | None: The unique identifier for the quiz.
        """
        return self.quiz_id


class QuizItem(BaseDomainModel):
    """The domain model for a quiz item.

    Attributes:
        quiz_item_id (int | None): The unique identifier for the quiz item.
        quiz_id (int): The unique identifier for the quiz that owns the quiz item.
        item_id (int): The unique identifier for the item that the quiz item is based on.
        question_number (int): The number of the question the quiz item in the quiz.
        choice_item_ids (list[int]): The list of unique identifiers of items that are used
            as choices for the question.
        correct_answer (int): The index of the correct answer in `choice_item_ids`.
        user_answer (int): The index of the user's answer in `choice_item_ids`.
        answer_time (int): The time (in seconds) taken by the user to answer the question.
    """

    quiz_item_id: int | None = None
    quiz_id: int
    item_id: int | None
    question_number: int
    choice_item_ids: list[int]
    correct_answer: int
    user_answer: int | None = None
    answer_time: int | None = None

    @property
    def self_id(self) -> int | None:
        """The alias of unique identifier for the quiz item.

        This property is required by the base repository, which is solely responsible for
        all CRUD operations.

        Returns:
            int | None: The unique identifier for the quiz item.
        """
        return self.quiz_item_id
