from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from src.application.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from src.application.mediator import Mediator
from src.infra.repositories.messages.base import BaseChatRepository
from src.infra.repositories.messages.mongo import MongoDBChatRepository
from src.settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(CreateChatCommandHandler)
    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )

        return mediator

    def init_chat_mongodb_repository():
        config: Config = container.resolve(Config)
        client = AsyncIOMotorClient(config.mongodb_connection_uri, serverSelectionTimeoutMS=3000)
        return MongoDBChatRepository(
            mongo_client=client,
            mongo_db_name=config.mongodb_chat_database,
            mongo_collection_name=config.mongodb_chat_collection,
        )

    container.register(BaseChatRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(Mediator, factory=init_mediator)

    return container
