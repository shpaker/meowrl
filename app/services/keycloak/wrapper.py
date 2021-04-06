from logging import getLogger
from typing import Optional

from keycloak import KeycloakOpenID

from app.services.base import ServiceWrapperBase
from app.services.keycloak.settings import KeycloakSettings

PUBLIC_KEY_WRAPPER = "-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
logger = getLogger(__name__)


class KeycloakWrapper(ServiceWrapperBase):
    def __init__(self) -> None:
        super().__init__()
        self.healthz_name: str = "keycloak"
        self.client: KeycloakOpenID
        self.public_key: Optional[str] = None
        self.settings: KeycloakSettings = KeycloakSettings()

    async def startup_event_handler(self) -> None:
        self.client = KeycloakOpenID(  # noqa
            server_url=self.settings.keycloak_server_url,
            client_id=self.settings.keycloak_client_id,
            realm_name=self.settings.keycloak_realm_name,
        )
        if not self.settings.keycloak_verify_signature:
            return
        raw_public_key = self.client.public_key()
        self.public_key = PUBLIC_KEY_WRAPPER.format(public_key=raw_public_key)
        logger.info(f"SSO public key received: {raw_public_key}")

    async def shutdown_event_handler(self) -> None:
        pass

    async def health_check(self) -> None:
        if not self.settings.keycloak_verify_signature:
            return
        assert self.public_key is not None
