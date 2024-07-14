from punq import (
    Container,
    Scope,
)

from src.infra.di.containers import _init_container
from src.infra.repositories.messages.base import BaseChatRepository
from src.infra.repositories.messages.memory import MemoryChatRepository


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    return container
