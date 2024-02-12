from datetime import datetime

from pydantic import BaseModel, PastDatetime, Field, AliasChoices
from pydantic.networks import IPvAnyAddress


class User(BaseModel):
    user_id: int | None = Field(default=None, validation_alias=AliasChoices("user_id", "self_id"))
    user_name: str
    email: str
    password: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: PastDatetime = datetime.now()
    updated_at: PastDatetime = datetime.now()


class UserLoginHistory(BaseModel):
    self_id: int
    user_id: int
    login_timestamp: PastDatetime
    logout_timestamp: PastDatetime
    ip_address: IPvAnyAddress
