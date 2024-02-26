# ruff: noqa: INP001
# This is necessary to ensure the models are all imported and registered.
from typing import cast

from db.models.sqlalchemy_data_models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.core.security import get_password_hash
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User


async def create_first_superuser() -> None:
    """Create the first superuser.

    This function creates the first superuser if it doesn't exist.
    """
    # Create a new async engine instance, which offers a session environment to manage a database.
    engine = create_async_engine(cast(str, settings.SQLALCHEMY_DATABASE_URI))

    # Create a factiry that returns a new AsyncSession instance.
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # Drop and create all tables defined as data models under `src/db`.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # This context automatically calls async_session.close() when the code block is exited.
    async with async_session_maker() as async_session:
        user_repository = UserRepository(async_session)
        # Check if the user already exists.
        user = await user_repository.read_by_email(settings.FIRST_SUPERUSER_EMAIL)
        # Create the first superuser if it doesn't exist.
        if user is None:
            print("Creating first superuser")
            user_in = User(
                user_name=settings.FIRST_SUPERUSER,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
            )
            await user_repository.create(user_in)
        else:
            print("First superuser already exists!")

    print("First superuser has successfully been created!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_first_superuser())
