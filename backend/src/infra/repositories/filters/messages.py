from dataclasses import dataclass


@dataclass
class MessagesFilter:
    offset: int = 0
    limit: int = 10
