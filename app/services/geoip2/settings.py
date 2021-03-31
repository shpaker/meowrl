from typing import Optional

from app.utils import ServiceSettingsBase


class GeoIp2Settings(ServiceSettingsBase):
    geoip2_account_id: Optional[int] = None
    geoip2_license_key: Optional[str] = None
    geoip2_use_geolite: bool = True
