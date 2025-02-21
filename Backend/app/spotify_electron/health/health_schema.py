"""
This module defines the schema for health check responses.

It includes the `HealthCheckResponse` model, which represents the structure
of responses for system health checks.
"""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Class that represents response of health check"""

    status: str
    details: dict[str, dict[str, str]]
