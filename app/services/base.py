from abc import ABC, abstractmethod
from asyncio import wait_for
from logging import getLogger

from fastapi import FastAPI
from pydantic import BaseSettings

from app.utils import SingletonABCMeta

logger = getLogger(__name__)


class ServiceWrapperBase(ABC, metaclass=SingletonABCMeta):
    def __init__(self, healthz_timeout: int = 8):
        logger.info(f"{self.__class__.__name__} instance created")
        self.healthz_timeout: int = healthz_timeout
        self.healthz_name: str = "service"
        self.settings: BaseSettings

    def add_event_handlers(self, app: FastAPI) -> None:
        app.add_event_handler("startup", self.startup_event_handler)
        app.add_event_handler("shutdown", self.shutdown_event_handler)

    @abstractmethod
    async def startup_event_handler(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def shutdown_event_handler(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> None:
        raise NotImplementedError

    async def health_check_call(self) -> bool:
        is_passed = False
        try:
            fut = self.health_check()
            if self.healthz_timeout:
                await wait_for(fut, timeout=self.healthz_timeout)
            else:
                await fut
            is_passed = True
        except TimeoutError:
            logger.critical(f"Exceeded the timeout of {self.healthz_timeout} seconds", exc_info=True)
        except Exception:  # noqa  # pylint: disable=broad-except
            logger.critical("Error occurred", exc_info=True)

        return is_passed
