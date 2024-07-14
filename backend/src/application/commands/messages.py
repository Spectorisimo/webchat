from dataclasses import dataclass

from src.application.commands.base import BaseCommand, CommandHandler
from src.application.exceptions.messages import ChatWithThisTitleAlreadyExistsException
from src.domain.entities.messages import Chat
from src.domain.value_objects.messages import Title
from src.infra.repositories.messages.base import BaseChatRepository


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThisTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)

        new_chat = Chat.create_chat(title=title)
        await self.chat_repository.add_chat(new_chat)

        return new_chat
