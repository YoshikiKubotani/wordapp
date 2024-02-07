from pydantic import BaseModel, PastDatetime
from pydantic.networks import IPvAnyAddress


class CreateUserRequest(BaseModel):
    user_name: str
    email: str
    full_name: str | None = None
    password: str

class UpdateUserRequest(BaseModel):
    user_name: str
    email: str
    full_name: str | None = None
    password: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    full_name: str


class User(BaseModel):
    user_name: str
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class DummyUser(User):
    user_id: int
    is_superuser: bool
    hashed_password: str


class UserSchema(BaseModel):
    _id: int
    user_name: str
    email: str
    password: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: PastDatetime
    updated_at: PastDatetime

class UserLoginHistorySchema(BaseModel):
    _id: int
    user_id: int
    login_timestamp: PastDatetime
    logout_timestamp: PastDatetime
    ip_address: IPvAnyAddress