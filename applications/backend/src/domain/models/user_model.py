from pydantic import BaseModel, PastDatetime
from pydantic.networks import IPvAnyAddress

class User(BaseModel):
    _id: int
    user_name: str
    email: str
    password: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: PastDatetime
    updated_at: PastDatetime


class UserLoginHistory(BaseModel):
    _id: int
    user_id: int
    login_timestamp: PastDatetime
    logout_timestamp: PastDatetime
    ip_address: IPvAnyAddress