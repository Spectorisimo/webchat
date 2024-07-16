from pydantic import BaseModel

from src.infra.repositories.filters.messages import MessagesFilter as MessagesInfraFilters


class MessagesFilter(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self) -> MessagesInfraFilters:
        return MessagesInfraFilters(
            limit=self.limit,
            offset=self.offset,
        )
