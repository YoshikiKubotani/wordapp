from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sqlalchemy_data_models import (
    SQLAlchemyDeck,
    SQLAlchemyGenre,
    SQLAlchemyItem,
    SQLAlchemyTest,
    SQLAlchemyTestItem,
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
)
from src.db.repositories.repository_interface import IRepository

DataModelType = TypeVar(
    "DataModelType",
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    SQLAlchemyDeck,
    SQLAlchemyGenre,
    SQLAlchemyItem,
    SQLAlchemyTest,
    SQLAlchemyTestItem,
)
DomainModelType = TypeVar("DomainModelType", bound=BaseModel)


class BaseRepository(
    Generic[DataModelType, DomainModelType], IRepository[AsyncSession, DomainModelType]
):
    def __init__(self, data_model: Type[DataModelType]) -> None:
        self.data_model = data_model

    async def create(
        self, async_session: AsyncSession, domain_entity: DomainModelType
    ) -> DomainModelType:
        # # This context automatically calls session.close() when the code block is exited.
        # async with async_session() as session:
        # This context automatically calls session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls session.rollback().
        async with async_session.begin():
            data_entity = self.data_model(**domain_entity.model_dump())
            async_session.add(data_entity)
            await async_session.flush()
            await async_session.refresh(data_entity)
        created_domain_entity = DomainModelType.model_validate(data_entity)
        return created_domain_entity

    async def read(self, async_session: AsyncSession, id: int) -> DomainModelType:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                data_entity = await session.get(self.data_model, id)
            read_domain_entity = DomainModelType.model_validate(data_entity)
            return read_domain_entity

    async def update(
        self, async_session: AsyncSession, domain_entity: DomainModelType
    ) -> DomainModelType:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                data_entity = await session.get(self.data_model, domain_entity._id)
                domain_entity_dict = domain_entity.model_dump(exlude_none=True)
                for key, value in domain_entity_dict.items():
                    setattr(data_entity, key, value)
                session.add(data_entity)
                await session.flush()
                await session.refresh(data_entity)
            updated_domain_entity = DomainModelType.model_validate(data_entity)
            return updated_domain_entity

    async def delete(self, async_session: AsyncSession, id: int) -> DomainModelType:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                data_entity = await session.get(self.data_model, id)
                session.delete(data_entity)
            deleted_domain_entity = DomainModelType.model_validate(data_entity)
            return deleted_domain_entity
