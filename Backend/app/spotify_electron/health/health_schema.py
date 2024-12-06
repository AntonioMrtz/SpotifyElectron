from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    """Class that represents response of health check"""
    status: str
    details: dict[str, dict[str, str]]