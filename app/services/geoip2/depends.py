from typing import Optional

import geoip2.webservice  # pylint: disable=import-error

from app.services.geoip2.wrapper import GeoIP2Wrapper


def get_geoip2_client() -> Optional[geoip2.webservice.AsyncClient]:
    wrapper = GeoIP2Wrapper()
    return wrapper.client
