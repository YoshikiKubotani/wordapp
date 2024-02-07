from typing import Any

from fastapi import APIRouter, HTTPException

from new_src.api.dependencies import AsyncSessionDep, CurrentUserDep
from new_src.api.schemas import CreateItemRequest, ItemResponse, UpdateItemRequest

router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
async def search_items(
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
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
async def create_item(
    # item: CreateItemRequest,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Create a new item."""
    return ItemResponse(
        item_id=1,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Get the details of an item."""
    return ItemResponse(
        item_id=item_id,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    # item: UpdateItemRequest,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> Any:
    """Update the details of an item."""
    return ItemResponse(
        item_id=item_id,
        english="dummy_english",
        japanese="dummy_japanese",
        grade=1
    )


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: CurrentUserDep,
    async_session: AsyncSessionDep,
) -> bool:
    """Delete an item."""
    return True
