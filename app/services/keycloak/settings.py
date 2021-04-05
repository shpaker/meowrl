from app.utils import ServiceSettingsBase


class KeycloakSettings(ServiceSettingsBase):
    keycloak_server_url: str
    keycloak_client_id: str
    keycloak_realm_name: str
    keycloak_verify_signature: bool = True
