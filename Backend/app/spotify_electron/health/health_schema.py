"""
This module defines the schemas for health-related API responses.

It includes data models and structures used for health checks and
related functionalities in the application.
"""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Class that represents response of health check"""

    status: str
    details: dict[str, dict[str, str]]
