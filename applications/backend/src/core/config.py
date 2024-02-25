import json
import secrets

from pydantic import (
    # AnyHttpUrl,
    EmailStr,
    PostgresDsn,
    ValidationInfo,
    field_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings, case_sensitive=True):
    """The settings for the application.

    Attributes:
        PROJECT_NAME (str): The name of the project.
        API_V1_STR (str): The base path for the API.
        SECRET_KEY (str): The secret key for the JWT signature.
        ALGORITHM (str): The algorithm used to encode and decode the JWT.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for the access token in minutes.
        BACKEND_CORS_ORIGINS (tuple[AnyHttpUrl]): The list of allowed origins for CORS.
        POSTGRES_SERVER (str): The name of the PostgreSQL server.
        POSTGRES_USER (str): The username for the PostgreSQL server.
        POSTGRES_PASSWORD (str): The password for the PostgreSQL server.
        POSTGRES_DB (str): The name of the PostgreSQL database.
        POSTGRES_SCHEMA (str): The name of the PostgreSQL schema.
        SQLALCHEMY_DATABASE_URI (PostgresDsn | None): The connection URI for the PostgreSQL database.
        TEST_USER_EMAIL (EmailStr): The email address of the test user.
        FIRST_SUPERUSER (str): The name of the first superuser.
        FIRST_SUPERUSER_EMAIL (EmailStr): The email address of the first superuser.
        FIRST_SUPERUSER_PASSWORD (str): The password of the first superuser.
    """

    PROJECT_NAME: str = "Word App"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:8080"]'
    BACKEND_CORS_ORIGINS: str

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def validate_cors_origins(cls, v: str) -> str:
        """Validate the BACKEND_CORS_ORIGINS field.

        Args:
            v (str): The value of the BACKEND_CORS_ORIGINS field.

        Raises:
            ValueError: If BACKEND_CORS_ORIGINS is invalid.

        Returns:
            list[str]: The validated value of the BACKEND_CORS_ORIGINS field.
        """
        try:
            parsed_data = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(
                "JSON decode failed. BACKEND_CORS_ORIGINS must be a JSON-formatted list."
            ) from e

        if isinstance(parsed_data, list) and all(
            isinstance(elem, str) for elem in parsed_data
        ):
            return v
        else:
            raise ValueError(
                "The decoded JSON was not a list of strings. BACKEND_CORS_ORIGINS must be a JSON-formatted list."
            )

    # celeryで使用するみたい
    # SENTRY_DSN: Optional[HttpUrl] = None
    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    POSTGRES_SERVER: str = "postgresql"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str = "public"

    # TODO: 設定対象ごとに別のSettingクラスを作る場合、ここはmodel_validatorにする
    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> str:
        """Assemble a Pydantic PostgresDsn object from environment variables.

        Args:
            v (str | None): The value of the SQLALCHEMY_DATABASE_URI field.
            info (ValidationInfo): The other fields of the Settings object.

        Returns:
            MultiHostUrl: The assembled PostgresDsn object.
        """
        if isinstance(v, str):
            return MultiHostUrl(v).unicode_string()
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host="postgresql",
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()

    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v

    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    # EMAILS_ENABLED: bool = False

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )

    TEST_USER_EMAIL: EmailStr = "test@gmail.com"
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    # USERS_OPEN_REGISTRATION: bool = False


settings = Settings()  # type: ignore
