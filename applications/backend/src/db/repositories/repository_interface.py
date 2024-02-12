from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

DomainModelType = TypeVar("DomainModelType", bound=BaseModel)

class IRepository(ABC, Generic[DomainModelType]):
    @abstractmethod
    async def create(
        self, domain_entity: DomainModelType
    ) -> DomainModelType:
        pass

    @abstractmethod
    async def read(self, id: int) -> DomainModelType:
        pass

    @abstractmethod
    async def update(self, domain_entity: DomainModelType) -> DomainModelType:
        pass

    @abstractmethod
    async def delete(self, id: int) -> DomainModelType:
        pass
