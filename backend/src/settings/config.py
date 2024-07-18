from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # MONGO
    mongodb_connection_uri: str = Field(alias='MONGO_DB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='chat', alias='MONGODB_CHAT_DATABASE')
    mongodb_chat_collection: str = Field(default='chat', alias='MONGODB_CHAT_COLLECTION')
    mongodb_message_collection: str = Field(default='message', alias='MONGODB_MESSAGE_COLLECTION')

    # KAFKA
    kafka_url: str = Field(alias='KAFKA_URL')

    new_chat_created_topic: str = Field(default='new_chat_created_topic')
    new_message_received_topic: str = Field(default='new_message_received_topic')
