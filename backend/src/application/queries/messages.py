from dataclasses import dataclass
from typing import Iterable

from src.application.exceptions.messages import ChatNotFoundException
from src.application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)
from src.domain.entities.messages import (
    Chat,
    Message,
)
from src.infra.repositories.filters.messages import MessagesFilter
from src.infra.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: MessagesFilter


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler):
    chat_repository: BaseChatRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    message_repository: BaseMessageRepository

    async def handle(self, query: GetMessagesQuery) -> tuple[Iterable[Message], int]:
        return await self.message_repository.get_messages_by_chat_oid(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
