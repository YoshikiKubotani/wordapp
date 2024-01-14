from typing import Any

from fastapi import APIRouter, HTTPException

from new_src.api.dependencies import CurrentUser # , SessionDep
from new_src.api.schemas import (
    CreateDeckRequest,
    CreateItemRequest,
    DeckResponse,
    ItemResponse,
)

router = APIRouter()


@router.get("/", response_model=list[DeckResponse])
def read_all_decks(
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Read all the decks registered by a user."""
    decks = [DeckResponse(deck_id=1, deck_name="dummy_deck")]
    return decks


@router.post("/", response_model=DeckResponse)
def create_deck(
    # deck: CreateDeckRequest,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Create a new deck."""
    return DeckResponse(deck_id=1, deck_name="dummy_deck")


@router.put("/{deck_id}", response_model=DeckResponse)
def update_deck(
    # deck_id: int,
    # deck: CreateDeckRequest,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Update the details of a deck."""
    return DeckResponse(deck_id=1, deck_name="dummy_deck")


@router.delete("/{deck_id}")
def delete_deck(
    # deck_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> bool:
    """Delete a deck."""
    return True


@router.get("/{deck_id}/items", response_model=list[ItemResponse])
def read_deck_items(
    # deck_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Get all the items in a deck."""
    items = [ItemResponse(item_id=1, item_name="dummy_item")]
    return items


@router.post("/{deck_id}/items", response_model=ItemResponse)
def create_deck_item(
    # deck_id: int,
    # item: CreateItemRequest,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Create a new item in a deck."""
    return ItemResponse(item_id=1, item_name="dummy_item")


@router.delete("/{deck_id}/items/{item_id}")
def delete_deck_item(
    # deck_id: int,
    # item_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> bool:
    """Delete an item from a deck."""
    return True
