from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class TextTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Too long message text "{self.text[:255]}..."'


@dataclass(frozen=True, eq=False)
class EmptyTextException(ApplicationException):

    @property
    def message(self):
        return f'Text can not be empty'
