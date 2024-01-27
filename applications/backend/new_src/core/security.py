from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from new_src.api.schemas import DummyUser, User
from new_src.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def authenticate_user(
    # session: SessionDep,
    user_name: str,
    password: str,
) -> User | None:
    # user_dict = session.get(User, user_name)
    # user = UserInDB(**user_dict)
    user = DummyUser(
        user_name=user_name,
        email="dummy@gmail.com",
        full_name="dummy user",
        is_active=True,
        is_superuser=True,
        hashed_password="$2b$12$gjLw4vccsNb41k/eHJeGtemKhjzw3aKxW6ANle2ZXzJTfhiRyvgNy",
    )
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt