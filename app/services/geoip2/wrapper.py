from logging import getLogger
from typing import Optional

import geoip2.webservice  # pylint: disable=import-error

from app.services.base import ServiceWrapperBase
from app.services.geoip2.settings import GeoIp2Settings

logger = getLogger(__name__)


class GeoIP2Wrapper(ServiceWrapperBase):
    def __init__(self) -> None:
        super().__init__()
        self.healthz_name = "geoip2"
        self.client: Optional[geoip2.webservice.AsyncClient] = None
        self.settings: GeoIp2Settings = GeoIp2Settings()

    async def startup_event_handler(self) -> None:
        if not self.settings.geoip2_account_id and not self.settings.geoip2_license_key:
            return
        params = dict(
            account_id=self.settings.geoip2_account_id,
            license_key=self.settings.geoip2_license_key,
        )
        if self.settings.geoip2_use_geolite:
            params.update(host="geolite.info")
        self.client = geoip2.webservice.AsyncClient(**params)  # type: ignore

    async def shutdown_event_handler(self) -> None:
        if self.client:
            await self.client.close()

    async def health_check(self) -> None:
        pass
