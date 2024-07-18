from faker import Faker

from src.domain.entities.messages import (
    Chat,
    Message,
)
from src.domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from src.domain.value_objects.messages import (
    Text,
    Title,
)


def test_create_message_success(faker: Faker):
    value = faker.text()[:100]

    text = Text(value=value)
    chat_oid = faker.uuid4()

    message = Message(text=text, chat_oid=chat_oid)
    assert message.text.value == value


def test_create_chat_success(faker: Faker):
    value = faker.text()[:100]

    title = Title(value=value)

    chat = Chat(title=title)
    assert chat.title.value == value


def test_add_message_to_chat(faker: Faker):
    value = faker.text()[:100]

    title = Title(value=value)

    text = Text(value=value)

    chat = Chat(title=title)
    message = Message(text=text, chat_oid=chat.oid)

    chat.add_message(message=message)

    assert message in chat.messages

    events = chat.pull_events()

    assert not chat._events
    assert len(events) == 1, events


def test_new_message_events(faker: Faker):
    value = faker.text()[:100]

    title = Title(value=value)

    text = Text(value=value)

    chat = Chat(title=title)
    message = Message(text=text, chat_oid=chat.oid)

    chat.add_message(message=message)
    events = chat.pull_events()

    assert not chat._events
    assert len(events) == 1, events

    new_message_receivded_event = events[0]

    assert isinstance(new_message_receivded_event, NewMessageReceivedEvent), new_message_receivded_event
    assert new_message_receivded_event.message_oid == message.oid
    assert new_message_receivded_event.message_text == message.text.to_raw()
    assert new_message_receivded_event.chat_oid == chat.oid


def test_new_chat_events(faker: Faker):
    value = faker.text()[:100]

    title = Title(value=value)

    chat = Chat.create_chat(title=title)
    events = chat.pull_events()

    assert not chat._events
    assert len(events) == 1, events

    new_chat_created_event = events[0]

    assert isinstance(new_chat_created_event, NewChatCreatedEvent), new_chat_created_event
    assert new_chat_created_event.chat_oid == chat.oid
    assert new_chat_created_event.chat_title == chat.title.to_raw()
