from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.repository_interface import IRepository
from db.models.sqlalchemy_data_models import (
    SQLAlchemyDeck,
    SQLAlchemyGenre,
    SQLAlchemyItem,
    SQLAlchemyQuiz,
    SQLAlchemyQuizItem,
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    orm_object_to_dict,
)

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
DomainModelType = TypeVar("DomainModelType", bound=BaseModel)


class BaseRepository(
    IRepository[DomainModelType], Generic[DataModelType, DomainModelType]
):
    def __init__(
        self, data_model: Type[DataModelType], domain_model: Type[DomainModelType], async_seesoon: AsyncSession
    ) -> None:
        self.data_model = data_model
        self.domain_model = domain_model
        self.async_session = async_seesoon

    async def create(self, domain_entity: DomainModelType) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = self.data_model(**domain_entity.model_dump())
            self.async_session.add(data_entity)
            await self.async_session.flush()
            await self.async_session.refresh(data_entity)
        data_entity_dict = orm_object_to_dict(data_entity)
        domain_entity = self.domain_model.model_validate(data_entity_dict)
        return domain_entity

    async def read(self, id: int) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = await self.async_session.get(self.data_model, id)
        data_entity_dict = orm_object_to_dict(data_entity)
        read_domain_entity = self.domain_model.model_validate(data_entity_dict)
        return read_domain_entity

    async def update(self, domain_entity: DomainModelType) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = await self.async_session.get(self.data_model, domain_entity.self_id)
            domain_entity_dict = domain_entity.model_dump(exlude_none=True)
            for key, value in domain_entity_dict.items():
                setattr(data_entity, key, value)
            self.async_session.add(data_entity)
            await self.async_session.flush()
            await self.async_session.refresh(data_entity)
        return domain_entity

    async def delete(self, id: int) -> DomainModelType:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            data_entity = await self.async_session.get(self.data_model, id)
            self.async_session.delete(data_entity)
        data_entity_dict = orm_object_to_dict(data_entity)
        deleted_domain_entity = self.domain_model.model_validate(data_entity_dict)
        return deleted_domain_entity
