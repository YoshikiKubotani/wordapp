from datetime import date, datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """The response for the health check endpoint.

    Attributes:
        status (str): The status of the health check.
    """

    status: Annotated[str, Field(..., description="The status of the health check.")]