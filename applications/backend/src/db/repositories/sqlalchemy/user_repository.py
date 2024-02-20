from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.sqlalchemy_data_models import (
    SQLAlchemyUser,
    SQLAlchemyUserLoginHistory,
    orm_object_to_dict,
)
from src.domain.models import User, UserLoginHistory

from .base_repository import BaseRepository


class UserRepository(BaseRepository[SQLAlchemyUser, User]):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(data_model=SQLAlchemyUser, domain_model=User, async_seesoon=async_session)

    async def read_by_username(self, user_name: str) -> User | None:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model).where(self.data_model.user_name == user_name)
            )
            user = results.scalars().one_or_none()
        if user is not None:
            user = User.model_validate(orm_object_to_dict(user))
        return user

    async def read_by_email(self, email: str) -> User | None:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls async_session.rollback().
        async with self.async_session.begin():
            results = await self.async_session.execute(
                select(self.data_model).where(self.data_model.email == email)
            )
            user = results.scalars().one_or_none()
        if user is not None:
            user = User.model_validate(orm_object_to_dict(user))
        return user


class UserLoginHistoryRepository(
    BaseRepository[SQLAlchemyUserLoginHistory, UserLoginHistory]
):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__(
            data_model=SQLAlchemyUserLoginHistory, domain_model=UserLoginHistory, async_seesoon=async_session
        )

    async def read_by_user_id(self, user_id: int) -> list[UserLoginHistory]:
        # This context automatically calls async_session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls session.rollback().
        async with self.async_session.begin():
            user_login_histories = await self.async_session.execute(
                select(self.data_model).where(self.data_model.user_id == user_id)
            )
            return user_login_histories.scalars().all()
