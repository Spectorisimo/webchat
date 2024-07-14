from dataclasses import dataclass

from src.domain.exceptions.messages import (
    EmptyTextException,
    TextTooLongException,
)

from .base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self) -> None:
        self._check_empty_message()

    def to_raw(self) -> str:
        return str(self.value)

    def _check_empty_message(self) -> None:
        if not self.value:
            raise EmptyTextException()


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self) -> None:
        self._check_empty_message()
        self._check_length_message()

    def to_raw(self) -> str:
        return str(self.value)

    def _check_empty_message(self) -> None:
        if not self.value:
            raise EmptyTextException()

    def _check_length_message(self) -> None:
        if len(self.value) > 255:
            raise TextTooLongException(self.value)
