from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from src.domain.events.base import BaseEvent
from src.infra.message_brokers.base import BaseMessageBroker
from src.infra.websocket.managers import BaseConnectionManager


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    connection_manager: BaseConnectionManager
    broker_topic: str | None = None

    def handle(self, event: ET) -> ER:
        ...
