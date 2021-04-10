😺 MEOWRL
===

Yet Another URL shortener service with authorization and simple statistics

---

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Environment settings

### Common settings

| Setting | Example | Description |
| :--- | :---: | :--- |
| MEOWRL_HOST | 0.0.0.0 | |
| MEOWRL_PORT | 8080 | |
| MEOWRL_DEBUG | True | |
| MEOWRL_ENABLE_SPECS | True | |

### MongoDB settings

| Setting | Example | Description |
| :--- | :---: | :--- |
| MEOWRL_MONGODB_DSN | `mongodb://root:example@localhost` | |

### KeyCloak settings

| Setting | Example | Description |
| :--- | :---: | :--- |
| MEOWRL_KEYCLOAK_VERIFY_SIGNATURE | True | |
| MEOWRL_KEYCLOAK_CLIENT_ID | test | |
| MEOWRL_KEYCLOAK_SERVER_URL | `http://127.0.0.1:8080/auth/` | |
| MEOWRL_KEYCLOAK_REALM_NAME | test | |

### GeoIP2 settings

| Setting | Example | Description |
| :--- | :---: | :--- |
| MEOWRL_GEOIP2_ACCOUNT_ID | 123456 | |
| MEOWRL_GEOIP2_LICENSE_KEY | qwerty | |
| MEOWRL_GEOIP2_USE_GEOLITE | True | |

### Sentry settings

| Setting | Example | Description |
| :--- | :---: | :--- |
| MEOWRL_SENTRY_DSN | `https://public@sentry.example.com/1` | |
