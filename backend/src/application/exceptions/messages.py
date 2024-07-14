from dataclasses import dataclass

from src.application.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class ChatWithThisTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Chat with given title already exists: {self.title}'
