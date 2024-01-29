from typing import TypeVar, Type
from pydantic import BaseModel

from new_src.api.dependencies import AsyncSessionDep
from new_src.db.data_models import User, Item, Genre, Deck, Test, TestItem, UserLoginHistory

DataModelType = TypeVar("DataModelType",  User, Item, Genre, Deck, Test, TestItem, UserLoginHistory)
DomainModelType = TypeVar("DomainModelType",  BaseModel)

class BaseRepository():
  def __init__(self, data_model: Type[DataModelType]) -> None:
    self.data_model = data_model

  async def create(self, async_session: AsyncSessionDep, domain_entity: DomainModelType) -> bool:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        data_entity = self.data_model(**domain_entity.model_dump())
        session.add(data_entity)
        await session.flush()
        await session.refresh(data_entity)
        return data_entity

  async def read(self, async_session: AsyncSessionDep, id: int) -> DomainModelType:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        data_entity = await session.get(self.data_model, id)
        return data_entity

  async def update(self, async_session: AsyncSessionDep, domain_entity: DomainModelType) -> bool:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        data_entity = await session.get(self.data_model, domain_entity.id)
        domain_entity_dict = domain_entity.model_dump(exlude_none=True)
        for key, value in domain_entity_dict.items():
          setattr(data_entity, key, value)
        session.add(data_entity)
        await session.flush()
        await session.refresh(data_entity)
        return data_entity


  async def delete(self, async_session: AsyncSessionDep, id: int) -> bool:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        data_entity = await session.get(self.data_model, id)
        session.delete(data_entity)
        return data_entity