from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import AsyncGenerator, Any


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes):
        ...

    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncGenerator[Any, None]:
        ...

    @abstractmethod
    async def stop_consuming(self):
        ...
