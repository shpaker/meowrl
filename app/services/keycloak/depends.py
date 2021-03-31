import logging
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.keycloak.models import JWTTokenModel
from app.services.keycloak.wrapper import KeycloakWrapper

sso = KeycloakWrapper()
http_bearer_scheme = HTTPBearer()


async def strict_bearer_auth(
    auth: HTTPAuthorizationCredentials = Depends(http_bearer_scheme),
) -> JWTTokenModel:
    try:
        payload = sso.client.decode_token(
            token=auth.credentials,
            key=sso.public_key,
            options=dict(
                verify_signature=sso.settings.keycloak_verify_signature,
                verify_aud=False,
                verify_exp=sso.settings.keycloak_verify_signature,
            ),
        )
    except Exception as err:
        logging.warning(f"{err.__class__.__name__} {err}: ")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    return JWTTokenModel(**payload)  # type: ignore


async def optional_bearer_auth(
    request: Request,
) -> Optional[JWTTokenModel]:
    if not request.headers.get("Authorization"):
        return None
    auth = await http_bearer_scheme(request)
    return await strict_bearer_auth(auth)  # type: ignore
