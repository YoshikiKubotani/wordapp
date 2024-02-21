from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field, PastDatetime
from pydantic.networks import IPvAnyAddress


class User(BaseModel):
    user_id: int | None = Field(
        default=None, validation_alias=AliasChoices("user_id", "self_id")
    )
    user_name: str
    email: str
    password: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: PastDatetime = datetime.now()
    updated_at: PastDatetime = datetime.now()


class UserLoginHistory(BaseModel):
    user_login_history_id: int | None = Field(
        default=None, validation_alias=AliasChoices("user_login_history_id", "self_id")
    )
    user_id: int
    login_timestamp: PastDatetime = datetime.now()
    logout_timestamp: PastDatetime = datetime.now()
    ip_address: IPvAnyAddress
