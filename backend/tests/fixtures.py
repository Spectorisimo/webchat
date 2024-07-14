from punq import Container, Scope

from src.infra.repositories.messages.base import BaseChatRepository
from src.infra.repositories.messages.memory import MemoryChatRepository
from src.infra.di.containers import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    return container
