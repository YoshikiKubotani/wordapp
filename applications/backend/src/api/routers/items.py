from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import async_session_dependency, current_user_dependency
from src.api.schemas import CreateItemRequest, ItemResponse, UpdateItemRequest

router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
async def search_items(
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Search for items."""
    items = [
        ItemResponse(
            item_id=1, english="dummy_english", japanese="dummy_japanese", grade=1
        )
    ]
    return items


@router.post("/", response_model=ItemResponse)
async def create_item(
    # item: CreateItemRequest,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Create a new item."""
    return ItemResponse(
        item_id=1, english="dummy_english", japanese="dummy_japanese", grade=1
    )


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Get the details of an item."""
    return ItemResponse(
        item_id=item_id, english="dummy_english", japanese="dummy_japanese", grade=1
    )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    # item: UpdateItemRequest,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> Any:
    """Update the details of an item."""
    return ItemResponse(
        item_id=item_id, english="dummy_english", japanese="dummy_japanese", grade=1
    )


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: current_user_dependency,
    async_session: async_session_dependency,
) -> bool:
    """Delete an item."""
    return True
