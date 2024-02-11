from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sqlalchemy_data_models import SQLAlchemyUser, SQLAlchemyUserLoginHistory
from src.domain.models import User, UserLoginHistory

from .base_repository import BaseRepository


class UserRepository(BaseRepository[SQLAlchemyUser, User]):
    def __init__(self) -> None:
        super().__init__(data_model=SQLAlchemyUser)

    async def read_by_username(
        self, async_session: AsyncSession, user_name: str
    ) -> User | None:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                user = await session.execute(
                    select(self.data_model).where(
                        self.data_model.user_name == user_name
                    )
                )
                return user.scalars().one_or_none()

    async def read_by_email(
        self, async_session: AsyncSession, email: str
    ) -> User | None:
        # This context automatically calls session.commit() if no exceptions are raised.
        # If an exception is raised, it automatically calls session.rollback().
        async with async_session.begin():
            results = await async_session.execute(
                select(self.data_model).where(
                    self.data_model.email == email
                )
            )
            user = results.scalars().one_or_none()
        if user is not None:
            user = User(
                _id=user.user_id,
                user_name=user.user_name,
                email=user.email,
                password=user.password,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        return user


class UserLoginHistoryRepository(
    BaseRepository[SQLAlchemyUserLoginHistory, UserLoginHistory]
):
    def __init__(self) -> None:
        super().__init__(data_model=SQLAlchemyUserLoginHistory)

    async def read_by_user_id(
        self, async_session: AsyncSession, user_id: int
    ) -> list[UserLoginHistory]:
        # This context automatically calls session.close() when the code block is exited.
        async with async_session() as session:
            # This context automatically calls session.commit() if no exceptions are raised.
            # If an exception is raised, it automatically calls session.rollback().
            async with session.begin():
                user_login_histories = await session.execute(
                    select(self.data_model).where(self.data_model.user_id == user_id)
                )
                return user_login_histories.scalars().all()
