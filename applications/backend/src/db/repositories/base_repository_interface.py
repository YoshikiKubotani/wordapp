from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

DomainModelType = TypeVar("DomainModelType", bound=BaseModel)


class IBaseRepository(ABC, Generic[DomainModelType]):
    """The base repository interface."""

    @abstractmethod
    async def create(self, domain_entity: DomainModelType) -> DomainModelType:
        """Create a new record in the database.

        Args:
            domain_entity (DomainModelType): The domain entity on which to base the new record.

        Returns:
            DomainModelType: The domain entity reconstructed from the newly created record.
        """
        pass

    @abstractmethod
    async def read(self, id: int) -> DomainModelType:
        """Read a record from the database.

        Args:
            id (int): The id of the record to read.

        Returns:
            DomainModelType: The domain entity created from the read record.
        """
        pass

    @abstractmethod
    async def update(self, domain_entity: DomainModelType) -> DomainModelType:
        """Update a record in the database.

        Args:
            domain_entity (DomainModelType): The domain entity used to update the record.

        Returns:
            DomainModelType: The domain entity reconstructed from the updated record.
        """
        pass

    @abstractmethod
    async def delete(self, id: int) -> DomainModelType:
        """Delete a record from the database.

        Args:
            id (int): The id of the record to delete.

        Returns:
            DomainModelType: The domain entity created from the deleted record.
        """
        pass
