from typing import Any

from fastapi import APIRouter, HTTPException

from new_src.api.dependencies import CurrentUserDep, AsyncSessionDep
from new_src.api.schemas import (
    CreateDeckRequest,
    CreateItemRequest,
    DeckResponse,
    ItemResponse,
)

router = APIRouter()


@router.get("/", response_model=list[DeckResponse])
async def read_all_decks(
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Read all the decks registered by a user."""
    decks = [DeckResponse(deck_id=1, deck_name="dummy_deck")]
    return decks


@router.post("/", response_model=DeckResponse)
async def create_deck(
    # deck: CreateDeckRequest,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Create a new deck."""
    return DeckResponse(deck_id=1, deck_name="dummy_deck")


@router.put("/{deck_id}", response_model=DeckResponse)
async def update_deck(
    deck_id: int,
    # deck: CreateDeckRequest,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Update the details of a deck."""
    return DeckResponse(deck_id=deck_id, deck_name="dummy_deck")


@router.delete("/{deck_id}")
async def delete_deck(
    deck_id: int,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> bool:
    """Delete a deck."""
    return True


@router.get("/{deck_id}/items", response_model=list[ItemResponse])
async def read_deck_items(
    deck_id: int,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Get all the items in a deck."""
    items = [ItemResponse(
        item_id=1,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )]
    return items


@router.post("/{deck_id}/items", response_model=ItemResponse)
async def create_deck_item(
    deck_id: int,
    # item: CreateItemRequest,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Create a new item in a deck."""
    return ItemResponse(
        item_id=1,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.delete("/{deck_id}/items/{item_id}")
async def delete_deck_item(
    deck_id: int,
    item_id: int,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> bool:
    """Delete an item from a deck."""
    return True
