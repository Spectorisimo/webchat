from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class LogicException(ApplicationException):
    @property
    def message(self):
        return 'Error occurred while request processing'
