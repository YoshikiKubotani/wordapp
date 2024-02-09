from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import UserLoginHistory, User
from src.db.data_models import SQLAlchemyUser, SQLAlchemyUserLoginHistory
from src.db.repositories.base_repository import BaseRepository


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
