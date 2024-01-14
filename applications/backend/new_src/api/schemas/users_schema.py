from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    email: str

class User(BaseModel):
    user_name: str
    email: str | None
    full_name: str | None
    disabled: bool | None

