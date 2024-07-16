from dataclasses import dataclass

from src.application.exceptions.messages import ChatNotFoundException
from src.application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)
from src.domain.entities.messages import Chat
from src.infra.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler):
    chat_repository: BaseChatRepository
    message_repository: BaseMessageRepository  # TODO: забирать сообщения отдельно

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        chat.messages = await self.message_repository.get_messages_by_chat_oid(chat.oid)

        return chat
