from dataclasses import dataclass

from src.application.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f'Not found handler for given event: {self.event_type}'


@dataclass(frozen=True, eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f'Not found handler for given command: {self.command_type}'
