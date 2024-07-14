import pytest
from faker import Faker
from tests.conftest import *  # noqa

from src.application.commands.messages import CreateChatCommand
from src.application.exceptions.messages import ChatWithThisTitleAlreadyExistsException
from src.application.mediator import Mediator
from src.domain.entities.messages import Chat
from src.domain.value_objects.messages import Title
from src.infra.repositories.messages.base import BaseChatRepository


@pytest.mark.asyncio
async def test_create_chat_command_success(
        chat_repository: BaseChatRepository,
        mediator: Mediator,
        faker: Faker,
):
    value_title = faker.text()[:25]
    chat = (await mediator.handle_command(CreateChatCommand(title=value_title)))[0]
    assert await chat_repository.check_chat_exists_by_title(title=chat.title.to_raw())


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
        chat_repository: BaseChatRepository,
        mediator: Mediator,
        faker: Faker,
):
    value_title = faker.text()[:25]
    chat = Chat(title=Title(value=value_title))
    await chat_repository.add_chat(chat=chat)

    with pytest.raises(ChatWithThisTitleAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=value_title))

    assert len(chat_repository._saved_chats) == 1
