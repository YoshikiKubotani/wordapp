from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    email: str

class User(BaseModel):
    user_name: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class DummyUser(User):
    hashed_password: str