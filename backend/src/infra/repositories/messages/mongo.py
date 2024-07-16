from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from motor.core import AgnosticClient

from src.domain.entities.messages import (
    Chat,
    Message,
)
from src.infra.repositories.filters.messages import MessagesFilter
from src.infra.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)
from src.infra.repositories.messages.converters import (
    convert_chat_document_to_entity,
    convert_chat_entity_to_document,
    convert_message_document_to_entity,
    convert_message_entity_to_document,
)


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_client: AgnosticClient
    mongo_db_name: str
    mongo_collection_name: str

    @property
    def _collection(self):
        return self.mongo_client[self.mongo_db_name][self.mongo_collection_name]


@dataclass
class MongoDBChatRepository(BaseChatRepository, BaseMongoDBRepository):

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return await self._collection.find_one(filter={'title': title})

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={'oid': oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def get_all_chats(self) -> Iterable[Chat]:
        cursor = self._collection.find()

        chats = [
            convert_chat_document_to_entity(chat_document=chat_document)
            async for chat_document in cursor
        ]

        return chats


@dataclass
class MongoDBMessageRepository(BaseMessageRepository, BaseMongoDBRepository):
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_entity_to_document(message),
        )

    async def get_messages_by_chat_oid(self, chat_oid: str, filters: MessagesFilter) -> tuple[Iterable[Message], int]:
        cursor = self._collection.find(filter={'chat_oid': chat_oid}).skip(filters.offset).limit(filters.limit).sort(
            {'created_at': -1},
        )

        messages = [
            convert_message_document_to_entity(message_document=message_document)
            async for message_document in cursor
        ]

        count = await self._collection.count_documents(filter={'chat_oid': chat_oid})

        return messages, count
