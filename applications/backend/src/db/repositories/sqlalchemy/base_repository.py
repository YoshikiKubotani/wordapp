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
from src.db.sqlalchemy_data_models import orm_object_to_dict

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
   IRepository[AsyncSession, DomainModelType], Generic[DataModelType, DomainModelType]
):
    def __init__(self, data_model: Type[DataModelType], domain_model: Type[DomainModelType]) -> None:
        self.data_model = data_model
        self.domain_model = domain_model

    async def create(
        self, async_session: AsyncSession, domain_entity: DomainModelType
    ) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with async_session.begin():
            data_entity = self.data_model(**domain_entity.model_dump())
            async_session.add(data_entity)
            await async_session.flush()
            await async_session.refresh(data_entity)
        data_entity_dict = orm_object_to_dict(data_entity)
        created_domain_entity = self.domain_model.model_validate(data_entity_dict)
        return created_domain_entity

    async def read(self, async_session: AsyncSession, id: int) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with async_session.begin():
            data_entity = await async_session.get(self.data_model, id)
        read_domain_entity = DomainModelType.model_validate(data_entity)
        return read_domain_entity

    async def update(
        self, async_session: AsyncSession, domain_entity: DomainModelType
    ) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with async_session.begin():
            data_entity = await async_session.get(self.data_model, domain_entity._id)
            domain_entity_dict = domain_entity.model_dump(exlude_none=True)
            for key, value in domain_entity_dict.items():
                setattr(data_entity, key, value)
            async_session.add(data_entity)
            await async_session.flush()
            await async_session.refresh(data_entity)
        updated_domain_entity = DomainModelType.model_validate(data_entity)
        return updated_domain_entity

    async def delete(self, async_session: AsyncSession, id: int) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with async_session.begin():
            data_entity = await async_session.get(self.data_model, id)
            async_session.delete(data_entity)
        deleted_domain_entity = DomainModelType.model_validate(data_entity)
        return deleted_domain_entity
