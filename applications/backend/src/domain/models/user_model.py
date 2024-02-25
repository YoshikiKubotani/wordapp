from datetime import datetime

from pydantic import BaseModel, PastDatetime
from pydantic.networks import IPvAnyAddress


class User(BaseModel):
    """The domain model for a user.

    Attributes:
        user_id (int | None): The unique identifier for the user.
        user_name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        full_name (str | None): The full name of the user.
        is_active (bool): The status of the user. True if active, False otherwise.
        is_superuser (bool): The role of the user. True if superuser, False otherwise.
        created_at (PastDatetime): The date and time when the user was created.
        updated_at (PastDatetime): The date and time when the user was last updated.
    """

    user_id: int | None = None
    user_name: str
    email: str
    password: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: PastDatetime = datetime.now()
    updated_at: PastDatetime = datetime.now()

    @property
    def self_id(self) -> int | None:
        """The alias of unique identifier for the user.

        This property is required by the base repository, which is solely responsible for
        all CRUD operations.

        Returns:
            int | None: The unique identifier for the user.
        """
        return self.user_id


class UserLoginHistory(BaseModel):
    """The domain model for a user login history.

    Attributes:
        user_login_history_id (int | None): The unique identifier for the user login history.
        user_id (int): The unique identifier for the user who logged in.
        login_timestamp (PastDatetime): The date and time when the user logged in.
        logout_timestamp (PastDatetime): The date and time when the user logged out.
        ip_address (IPvAnyAddress): The IP address of the user.
    """

    user_login_history_id: int | None = None
    user_id: int
    login_timestamp: PastDatetime = datetime.now()
    logout_timestamp: PastDatetime = datetime.now()
    ip_address: IPvAnyAddress

    @property
    def self_id(self) -> int | None:
        """The alias of unique identifier for the user login history.

        This property is required by the base repository, which is solely responsible for
        all CRUD operations.

        Returns:
            int | None: The unique identifier for the user login history.
        """
        return self.user_login_history_id
