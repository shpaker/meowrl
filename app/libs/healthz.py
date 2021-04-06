import sys
from datetime import timedelta
from logging import getLogger
from time import time
from typing import Tuple

from starlette.background import BackgroundTasks

from app.models.routers.healthz import HealthzCallSchema, HealthzResponseSchema
from app.services.base import ServiceWrapperBase

logger = getLogger(__name__)


async def shutdown_service() -> None:
    sys.exit(1)


async def call_health_checks(
    health_checks: Tuple[ServiceWrapperBase],
    background_tasks: BackgroundTasks,
) -> HealthzResponseSchema:
    response = HealthzResponseSchema()

    for wrapper in health_checks:
        started_at = time()
        passed = await wrapper.health_check_call()
        finished_at = time() - started_at  # noqa, type: ignore
        elapsed_time = timedelta(seconds=finished_at)

        if not passed:
            logger.error(f"Health check failed: {wrapper.healthz_name}")
            response.healthy = False

        response.checks[wrapper.healthz_name] = HealthzCallSchema(passed=passed, elapsed=elapsed_time)

    if not response.healthy:
        background_tasks.add_task(shutdown_service)
    return response
