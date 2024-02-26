from .base_model import BaseDomainModel


class Deck(BaseDomainModel):
    """The domain model for a deck.

    Attributes:
        deck_id (int | None): The unique identifier for the deck.
        user_id (int): The unique identifier for the user who owns the deck.
        deck_name (str): The name of the deck.
    """

    deck_id: int | None = None
    user_id: int
    deck_name: str

    @property
    def self_id(self) -> int | None:
        """The alias of unique identifier for the deck.

        This property is required by the base repository, which is solely responsible for
        all CRUD operations.

        Returns:
            int | None: The unique identifier for the deck.
        """
        return self.deck_id
