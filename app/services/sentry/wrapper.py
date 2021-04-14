import sentry_sdk

from app.services.base import ServiceWrapperBase
from app.services.sentry.settings import SentrySettings


class SentryWrapper(ServiceWrapperBase):
    def __init__(self) -> None:
        super().__init__()
        self.healthz_name = "sentry"
        self.settings: SentrySettings = SentrySettings()

    async def startup_event_handler(self) -> None:
        settings = SentrySettings()
        if settings.sentry_dsn:
            sentry_sdk.init(  # pylint: disable=abstract-class-instantiated
                dsn=settings.sentry_dsn,
                environment=settings.sentry_environment,
                release=settings.sentry_release,
                server_name=settings.sentry_server_name if settings.sentry_server_name else settings.sentry_environment,
            )

    async def shutdown_event_handler(self) -> None:
        ...

    async def health_check(self) -> None:
        ...
