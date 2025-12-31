# ruff: noqa: N802
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """The settings for the application.

    Attributes:
        CORS_ALLOW_ORIGINS (list[str]): The origins that are allowed to make requests to the API.
        DATABASE: Database configuration settings.
        COGNITO: AWS Cognito configuration for JWT authentication.
        ENABLE_AUTH: Whether to enable authentication (set to False for local development).
    """

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_nested_delimiter="__",
    )

    # CORS_ALLOW_ORIGINS is a list of origins that are allowed to make requests to the API.
    # e.g: ["http://localhost", "http://localhost:3000"]
    CORS_ALLOW_ORIGINS: list[str]

    @field_validator("CORS_ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Allow CORS_ALLOW_ORIGINS to be a JSON array or a comma-separated string.

        Args:
            v: The value to parse, either a string or a list of strings.
        """
        if isinstance(v, str):
            import json

            parsed = json.loads(v)
            # Ensure the parsed result is a list of strings
            if isinstance(parsed, list) and all(
                isinstance(item, str) for item in parsed
            ):
                return parsed
            raise ValueError(f"Expected list of strings, got {type(parsed)}")
        if isinstance(v, list) and all(isinstance(item, str) for item in v):
            return v
        raise ValueError(f"Expected list of strings, got {type(v)}")


settings = Settings()
