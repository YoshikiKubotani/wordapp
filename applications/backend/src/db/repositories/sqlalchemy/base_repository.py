from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyDeck,
    SQLAlchemyGenre,
    SQLAlchemyItem,
    SQLAlchemyQuiz,
    SQLAlchemyQuizItem,
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    orm_object_to_dict,
)
from src.db.repositories.base_repository_interface import IBaseRepository
from src.domain.models.base_model import BaseDomainModel

DataModelType = TypeVar(
    "DataModelType",
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    SQLAlchemyDeck,
    SQLAlchemyGenre,
    SQLAlchemyItem,
    SQLAlchemyQuiz,
    SQLAlchemyQuizItem,
)
DomainModelType = TypeVar("DomainModelType", bound=BaseDomainModel)


class BaseRepository(
    IBaseRepository[DomainModelType], Generic[DataModelType, DomainModelType]
):
    """The base class for all SQLAlchemy repositories."""

    def __init__(
        self,
        data_model: Type[DataModelType],
        domain_model: Type[DomainModelType],
        async_seesoon: AsyncSession,
    ) -> None:
        """Initialize the repository.

        Args:
            data_model (Type[DataModelType]): The SQLAlchemy data model.
            domain_model (Type[DomainModelType]): The domain model.
            async_seesoon (AsyncSession): The asynchronous session to use for database operations.
        """
        self.data_model = data_model  # type: ignore
        self.domain_model = domain_model
        self.async_session = async_seesoon

    async def create(self, domain_entity: DomainModelType) -> DomainModelType:
        """Create a new record in the database.

        Args:
            domain_entity (DomainModelType): The domain entity on which to base the new record.

        Returns:
            DomainModelType: The domain entity reconstructed from the newly created record.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = self.data_model(**domain_entity.model_dump())
            self.async_session.add(data_entity)
        data_entity_dict = orm_object_to_dict(data_entity)
        domain_entity = self.domain_model.model_validate(data_entity_dict)
        return domain_entity

    async def read(self, id: int) -> DomainModelType:
        """Read a record from the database.

        Args:
            id (int): The id of the record to read.

        Returns:
            DomainModelType: The domain entity created from the read record.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = await self.async_session.get(self.data_model, id)
        if data_entity is None:
            raise ValueError(
                f'The data with id {id} should be found in the "{self.data_model.__tablename__}" table \
                to read, but it was not found.'
            )
        data_entity_dict = orm_object_to_dict(data_entity)
        read_domain_entity = self.domain_model.model_validate(data_entity_dict)
        return read_domain_entity

    async def update(self, domain_entity: DomainModelType) -> DomainModelType:
        """Update a record in the database.

        Args:
            domain_entity (DomainModelType): The domain entity used to update the record.

        Returns:
            DomainModelType: The domain entity reconstructed from the updated record.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = await self.async_session.get(
                self.data_model, domain_entity.self_id
            )
            if data_entity is None:
                raise ValueError(
                    f'The data with id {domain_entity.self_id} should be found \
                    in the "{self.data_model.__tablename__}" table to update, but it was not found.'
                )
            domain_entity_dict = domain_entity.model_dump(exclude_none=True)
            for key, value in domain_entity_dict.items():
                setattr(data_entity, key, value)
            self.async_session.add(data_entity)
        return domain_entity

    async def delete(self, id: int) -> DomainModelType:
        """Delete a record from the database.

        Args:
            id (int): The id of the record to delete.

        Returns:
            DomainModelType: The domain entity created from the deleted record.
        """
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = await self.async_session.get(self.data_model, id)
            if data_entity is None:
                raise ValueError(
                    f'The data with id {id} should be found in the "{self.data_model.__tablename__}" table \
                    to delete, but it was not found.'
                )
            await self.async_session.delete(data_entity)
        data_entity_dict = orm_object_to_dict(data_entity)
        deleted_domain_entity = self.domain_model.model_validate(data_entity_dict)
        return deleted_domain_entity
