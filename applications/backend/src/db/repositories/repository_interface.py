from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

DomainModelType = TypeVar("DomainModelType", BaseModel)
# Add available types for asynchronous session if a new orm library is implemented
AsyncSessionType = TypeVar("AsyncSessionType", AsyncSession)


class IRepository(ABC, Generic[AsyncSessionType]):
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
