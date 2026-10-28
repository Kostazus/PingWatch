
from typing import Protocol, Optional
from app.domain.models import Monitor


class MonitorRepository(Protocol):
    async def add(self, monitor: Monitor) -> Monitor:
        ...

    async def get(self, monitor_id: int) -> Optional[Monitor]:
        ...

    async def list_by_owner(self, owner_id: int) -> list[Monitor]:
        ...

    async def update(self, monitor: Monitor) -> Monitor:
        ...

    async def delete(self, monitor_id: int) -> bool:
        ...
