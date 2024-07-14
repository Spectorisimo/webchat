from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from src.application.commands.base import CommandHandler, CT, CR, BaseCommand
from src.application.events.base import EventHandler, ET, ER
from src.application.exceptions.mediator import EventHandlersNotRegisteredException, \
    CommandHandlersNotRegisteredException
from src.domain.events.base import BaseEvent


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(self, command: type[CT], command_handlers: Iterable[CommandHandler[CT, CR]]) -> None:
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type=command_type)

        return [await handler.handle(command=command) for handler in handlers]
