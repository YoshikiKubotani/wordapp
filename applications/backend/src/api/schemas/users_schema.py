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
    user_name: str
    email: str
    full_name: str
