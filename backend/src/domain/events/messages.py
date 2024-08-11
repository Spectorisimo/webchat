from dataclasses import dataclass
from typing import ClassVar

from src.domain.events.base import (
    BaseEvent,
    IntegrationEvent,
)


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    chat_title: str


@dataclass
class NewMessageReceivedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = 'New Message From Broker Received'

    message_text: str
    message_oid: str
    chat_oid: str
