from dataclasses import dataclass, field

from src.domain.entities.base import BaseEntity
from src.domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from src.domain.value_objects.messages import Text, Title


@dataclass(eq=False)
class Message(BaseEntity):
    text: Text


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreated(
                chat_oid=new_chat.oid,
                chat_title=new_chat.title.to_raw()
            )
        )
        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.to_raw(),
                chat_oid=self.oid,
                message_oid=message.oid,
            )
        )
