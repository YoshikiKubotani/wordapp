from datetime import datetime

from pydantic import BaseModel, PastDatetime


class Item(BaseModel):
    """The domain model for an item.

    Attributes:
        item_id (int | None): The unique identifier for the item.
        user_id (int): The unique identifier for the user who owns the item.
        english (str): The English word or phrase.
        japanese (str): The Japanese translation.
        grade (int): The grade of the item. 0 (junior high school 1st grade) to 7 (university level).
        created_at (PastDatetime): The date and time when the item was created.
        updated_at (PastDatetime): The date and time when the item was last updated.
    """

    item_id: int | None = None
    user_id: int
    english: str
    japanese: str
    grade: int
    created_at: PastDatetime = datetime.now()
    updated_at: PastDatetime = datetime.now()

    @property
    def self_id(self) -> int | None:
        """The alias of unique identifier for the item.

        This property is required by the base repository, which is solely responsible for
        all CRUD operations.

        Returns:
            int | None: The unique identifier for the item.
        """
        return self.item_id
