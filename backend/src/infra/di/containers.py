from functools import lru_cache

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
from src.application.mediator.base import Mediator
from src.application.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)
from src.infra.repositories.messages.base import (
    BaseChatRepository,
    BaseMessageRepository,
)
from src.infra.repositories.messages.mongo import (
    MongoDBChatRepository,
    MongoDBMessageRepository,
)
from src.settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_chat_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatRepository(
            mongo_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_collection_name=config.mongodb_chat_collection,
        )

    def init_message_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBMessageRepository(
            mongo_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_collection_name=config.mongodb_message_collection,
        )

    container.register(BaseChatRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessageRepository, factory=init_message_mongodb_repository, scope=Scope.singleton)

    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def init_mediator():
        mediator = Mediator()

        # Commands
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )

        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)],
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

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
