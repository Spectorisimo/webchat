from punq import Container
from pytest import fixture

from src.application.mediator import Mediator
from src.infra.repositories.messages.base import BaseChatRepository

from .fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)
