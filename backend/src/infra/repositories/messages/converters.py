from src.domain.entities.messages import Chat, Message


def convert_message_entity_to_document(message: Message) -> dict:
    return {
        'oid': message.oid,
        'text': message.text.to_raw(),

    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        'oid': chat.oid,
        'title': chat.title.to_raw(),
        'created_at': chat.created_at,
        'messages': [convert_message_entity_to_document(message) for message in chat.messages],
    }
