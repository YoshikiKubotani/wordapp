from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

DomainModelType = TypeVar("DomainModelType", bound=BaseModel)
# TODO: Remove Callable from AsyncSessionType if a new orm library is implemented.  This is inserted only to avoid "A single constraint is not allowed" error.
# Add available types for asynchronous session if a new orm library is implemented
AsyncSessionType = TypeVar("AsyncSessionType", AsyncSession, Callable)


class IRepository(ABC, Generic[AsyncSessionType, DomainModelType]):
    @abstractmethod
    async def create(
        self, async_session: AsyncSessionType, domain_entity: DomainModelType
    ) -> DomainModelType:
        pass

    @abstractmethod
    async def read(self, async_session: AsyncSessionType, id: int) -> DomainModelType:
        pass

    @abstractmethod
    async def update(
        self, async_session: AsyncSessionType, domain_entity: DomainModelType
    ) -> DomainModelType:
        pass

    @abstractmethod
    async def delete(self, async_session: AsyncSessionType, id: int) -> DomainModelType:
        pass
