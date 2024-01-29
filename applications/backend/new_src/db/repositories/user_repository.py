from sqlalchemy import select

from new_src.db.repositories.base_repository import BaseRepository, AsyncSessionDep
from new_src.db.data_models import User, UserLoginHistory
from new_src.api.schemas import UserSchema, UserLoginHistorySchema

class UserRepository(BaseRepository):
  def __init__(self) -> None:
    super().__init__(data_model=User)
  
  async def read_by_username(self, async_session: AsyncSessionDep, user_name: str) -> UserSchema | None:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        user = await session.execute(select(self.data_model).where(self.data_model.user_name == user_name))
        return user.scalars().one_or_none()
      
class UserLoginHistoryRepository(BaseRepository):
  def __init__(self) -> None:
    super().__init__(data_model=UserLoginHistory)
  
  async def read_by_user_id(self, async_session: AsyncSessionDep, user_id: int) -> list[UserLoginHistorySchema]:
    # This context automatically calls session.close() when the code block is exited.
    async with async_session() as session:
      # This context automatically calls session.commit() if no exceptions are raised.
      # If an exception is raised, it automatically calls session.rollback().
      async with session.begin():
        user_login_histories = await session.execute(select(self.data_model).where(self.data_model.user_id == user_id))
        return user_login_histories.scalars().all()