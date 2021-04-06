from datetime import timedelta
from typing import Dict

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    name: str
    version: str


class HealthzCallSchema(BaseModel):
    passed: bool
    elapsed: timedelta


class HealthzResponseSchema(BaseModel):
    healthy: bool = True
    checks: Dict[str, HealthzCallSchema] = Field(default_factory=dict)
