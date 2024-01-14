from typing import Any

from fastapi import APIRouter, HTTPException

from new_src.api.dependencies import CurrentUser #, SessionDep
from new_src.api.schemas import CreateItemRequest, ItemResponse, UpdateItemRequest

router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
def search_items(
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Search for items."""
    items = [ItemResponse(
        item_id=1,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )]
    return items


@router.post("/", response_model=ItemResponse)
def create_item(
    # item: CreateItemRequest,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Create a new item."""
    return ItemResponse(
        item_id=1,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(
    item_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Get the details of an item."""
    return ItemResponse(
        item_id=item_id,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    # item: UpdateItemRequest,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> Any:
    """Update the details of an item."""
    return ItemResponse(
        item_id=item_id,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    # current_user: User = Depends(get_current_user),
    # session: Session = Depends(get_session),
) -> bool:
    """Delete an item."""
    return True
