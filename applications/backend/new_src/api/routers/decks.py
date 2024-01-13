from typing import Any

from fastapi import APIRouter, HTTPException

from new_src.api.dependencies import CurrentUser, SessionDep
from new_src.api.schemas import DeckOut, ItemCreate, ItemOut, ItemUpdate

router = APIRouter()

@router.get("/", response_model=list[DeckOut])
def read_all_decks(
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Read all the decks registered by a user."""
    decks = [DeckOut(deck_id=1, deck_name="dummy_deck")]
    return decks

@router.post("/", response_model=DeckOut)
def create_deck(
    # deck: DeckCreate,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Create a new deck."""
    return DeckOut(deck_id=1, deck_name="dummy_deck")

@router.get("/{deck_id}", response_model=DeckOut)
def read_deck(
    # deck_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Get the details of a deck."""
    return DeckOut(deck_id=1, deck_name="dummy_deck")

@router.put("/{deck_id}", response_model=DeckOut)
def update_deck(
    # deck_id: int,
    # deck: DeckUpdate,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Update the details of a deck."""
    return DeckOut(deck_id=1, deck_name="dummy_deck")

@router.delete("/{deck_id}")
def delete_deck(
    # deck_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> bool:
    """Delete a deck."""
    return True

@router.get("/{deck_id}/items", response_model=list[ItemOut])
def read_deck_items(
    # deck_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Get all the items in a deck."""
    items = [ItemOut(item_id=1, item_name="dummy_item")]
    return items

@router.post("/{deck_id}/items", response_model=ItemOut)
def create_deck_item(
    # deck_id: int,
    # item: ItemCreate,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Create a new item in a deck."""
    return ItemOut(item_id=1, item_name="dummy_item")

@router.delete("/{deck_id}/items/{item_id}")
def delete_deck_item(
    # deck_id: int,
    # item_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> bool:
    """Delete an item from a deck."""
    return True