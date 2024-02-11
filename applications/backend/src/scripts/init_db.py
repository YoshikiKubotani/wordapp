# This is necessary to ensure the models are all imported and registered.
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.core.security import get_password_hash
from src.db.repositories.sqlalchemy.user_repository import UserRepository
from src.domain.models import User


async def create_first_superuser() -> None:
    # Create a new async engine instance, which offers a session environment to manage a database.
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())

    # Create a factiry that returns a new AsyncSession instance.
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # This context automatically calls async_session.close() when the code block is exited.
    async with async_session_maker as async_session:
        user_repository = UserRepository()
        # Check if the user already exists.
        user = await user_repository.read_by_email(
            async_session, settings.FIRST_SUPERUSER_EMAIL
        )
        # Create the first superuser if it doesn't exist.
        if user is None:
            print("Creating first superuser")
            user_in = User(
                user_name=settings.FIRST_SUPERUSER,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
            )
            await user_repository.create(async_session, user_in)
        else:
            print("First superuser already exists!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_first_superuser())
