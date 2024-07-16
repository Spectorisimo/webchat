from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from src.domain.entities.messages import (
    Chat,
    Message,
)


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        ...

    @abstractmethod
    async def get_all_chats(self) -> Iterable[Chat]:
        ...


@dataclass
class BaseMessageRepository(ABC):

    @abstractmethod
    async def add_message(self, message: Message) -> None:
        ...

    @abstractmethod
    async def get_messages_by_chat_oid(self, chat_oid: str) -> Iterable[Message]:
        ...
