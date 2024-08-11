from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from src.application.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from src.application.events.messages import (
    NewChatCreatedEventHandler,
    NewMessageReceivedEventHandler,
    NewMessageReceivedFromBrokerEventHandler,
)
from src.application.mediator.base import Mediator
from src.application.mediator.event import EventMediator
from src.application.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from src.domain.events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
    NewMessageReceivedFromBrokerEvent,
)
from src.infra.message_brokers.base import BaseMessageBroker
from src.infra.message_brokers.kafka import KafkaMessageBroker
from src.infra.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)
from src.infra.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessageRepository,
)
from src.infra.websocket.managers import (
    BaseConnectionManager,
    ConnectionManager,
)
from src.settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def init_chat_mongodb_repository():
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatRepository(
            mongo_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_collection_name=config.mongodb_chat_collection,
        )

    def init_message_mongodb_repository():
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBMessageRepository(
            mongo_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_collection_name=config.mongodb_message_collection,
        )

    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_url,
                group_id=f"chats-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    container.register(BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton)

    container.register(BaseConnectionManager, instance=ConnectionManager(), scope=Scope.singleton)

    container.register(BaseChatRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessageRepository, factory=init_message_mongodb_repository, scope=Scope.singleton)

    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def init_mediator():
        mediator = Mediator()

        # Commands
        create_chat_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
        )
        create_message_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessageRepository),
            chat_repository=container.resolve(BaseChatRepository),
        )

        mediator.register_command(
            CreateChatCommand,
            [create_chat_handler],
        )

        mediator.register_command(
            CreateMessageCommand,
            [create_message_handler],
        )

        # Queries
        mediator.register_query(
            GetChatDetailQuery,
            container.resolve(GetChatDetailQueryHandler),
        )

        mediator.register_query(
            GetMessagesQuery,
            container.resolve(GetMessagesQueryHandler),
        )

        # Events
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            broker_topic=config.new_chat_created_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )
        new_message_received_handler = NewMessageReceivedEventHandler(
            broker_topic=config.new_message_received_topic,
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
        )

        new_message_received_from_broker_event_handler = NewMessageReceivedFromBrokerEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            broker_topic=config.new_message_received_topic,
            connection_manager=container.resolve(BaseConnectionManager),
        )

        mediator.register_event(
            NewChatCreatedEvent,
            [new_chat_created_event_handler],
        )
        mediator.register_event(
            NewMessageReceivedEvent,
            [new_message_received_handler],
        )
        mediator.register_event(
            NewMessageReceivedFromBrokerEvent,
            [new_message_received_from_broker_event_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    container.register(Scheduler, instance=Scheduler(), scope=Scope.singleton)

    return container
