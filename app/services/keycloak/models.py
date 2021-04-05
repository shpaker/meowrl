from datetime import datetime

from pydantic import UUID4, BaseModel


class JWTTokenModel(
    BaseModel,
):
    sub: UUID4
    azp: str
    exp: datetime
    iat: datetime
    preferred_username: str
