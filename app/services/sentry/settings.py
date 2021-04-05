from typing import Optional

from pydantic import AnyUrl

from app.utils import ServiceSettingsBase


class SentrySettings(ServiceSettingsBase):
    sentry_dsn: Optional[AnyUrl] = None
    sentry_environment: Optional[str] = None
    sentry_release: Optional[str] = None
    sentry_server_name: Optional[str] = None
