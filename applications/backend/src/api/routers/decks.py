from typing import Any

from fastapi import APIRouter

from src.api.dependencies import async_session_dependency, current_user_dependency
from src.api.schemas import (
    CreateDeckRequest,
    CreateItemRequest,
    DeckResponse,
    ItemResponse,
)
from src.db.repositories.sqlalchemy.deck_repository import DeckRepository
from src.domain.models import Deck

router = APIRouter()


@router.get("/", response_model=list[DeckResponse])
async def read_all_decks(
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Read all the decks registered by a user.

    Args:
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        list[DeckResponse]: The list of decks.
    """
    decks = [DeckResponse(deck_id=1, deck_name="dummy_deck")]
    return decks


@router.post("/", response_model=DeckResponse)
async def create_deck(
    deck: CreateDeckRequest,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Create a new deck.

    Args:
        deck (CreateDeckRequest): The deck to create.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        DeckResponse: The created deck.
    """
    entity = Deck(user_id=1, deck_name=deck.deck_name)
    repo = DeckRepository(async_session)
    created_deck = await repo.create(entity)
    return DeckResponse(deck_id=created_deck.deck_id, deck_name=created_deck.deck_name)  # type: ignore


@router.put("/{deck_id}", response_model=DeckResponse)
async def update_deck(
    deck_id: int,
    deck: CreateDeckRequest,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Update the details of a deck.

    Args:
        deck_id (int): The deck id.
        deck (CreateDeckRequest): The deck to update.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        DeckResponse: The updated deck.
    """
    return DeckResponse(deck_id=deck_id, deck_name="dummy_deck")


@router.delete("/{deck_id}")
async def delete_deck(
    deck_id: int,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> bool:
    """Delete a deck.

    Args:
        deck_id (int): The deck id.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        bool: True if the deck was deleted successfully.
    """
    return True


@router.get("/{deck_id}/items", response_model=list[ItemResponse])
async def read_deck_items(
    deck_id: int,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Get all the items in a deck.

    Args:
        deck_id (int): The deck id.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        list[ItemResponse]: The list of deck items.
    """
    items = [
        ItemResponse(
            item_id=1, english="dummy_english", japanese="dummy_japanese", grade=1
        )
    ]
    return items


@router.post("/{deck_id}/items", response_model=ItemResponse)
async def create_deck_item(
    deck_id: int,
    item: CreateItemRequest,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Create a new item in a deck.

    Args:
        deck_id (int): The deck id.
        item (CreateItemRequest): The item to create.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        ItemResponse: The created item.
    """
    return ItemResponse(
        item_id=1, english="dummy_english", japanese="dummy_japanese", grade=1
    )


@router.delete("/{deck_id}/items/{item_id}")
async def delete_deck_item(
    deck_id: int,
    item_id: int,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> bool:
    """Delete an item from a deck.

    Args:
        deck_id (int): The deck id.
        item_id (int): The item id.
        current_user (User): The current user.
        async_session (AsyncSession): The async session.

    Returns:
        bool: True if the item was deleted successfully.
    """
    return True
