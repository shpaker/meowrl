from app.services.geoip2.wrapper import GeoIP2Wrapper
from app.services.keycloak.wrapper import KeycloakWrapper
from app.services.mongodb.wrapper import MongoDBWrapper
from app.services.sentry.wrapper import SentryWrapper

SERVICE_WRAPPERS = (
    MongoDBWrapper(),
    KeycloakWrapper(),
    GeoIP2Wrapper(),
    SentryWrapper(),
)
SERVICE_HEALTH_CHECKS = (
    MongoDBWrapper(),
    KeycloakWrapper(),
)

__all__ = (
    "SERVICE_WRAPPERS",
    "SERVICE_HEALTH_CHECKS",
)
