from pydantic import BaseModel

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
    email: str


class User(BaseModel):
    user_name: str
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class DummyUser(User):
    hashed_password: str
