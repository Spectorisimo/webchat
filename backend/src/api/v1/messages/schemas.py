from datetime import datetime

from pydantic import BaseModel

from src.api.schemas import BaseQueryResponseSchema
from src.domain.entities.messages import (
    Chat,
    Message,
)


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.to_raw(),
            created_at=chat.created_at,
        )


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(
            text=message.text.to_raw(),
            oid=message.oid,
            created_at=message.created_at,
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> 'MessageDetailSchema':
        return cls(
            oid=message.oid,
            text=message.text.to_raw(),
            created_at=message.created_at,
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    messages: list[MessageDetailSchema]
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.to_raw(),
            messages=[MessageDetailSchema.from_entity(message) for message in chat.messages],
            created_at=chat.created_at,
        )


class MessagesResponseSchema(BaseQueryResponseSchema[list[MessageDetailSchema]]):
    ...
