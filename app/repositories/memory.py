from typing import Optional
from app.domain.models import Monitor
from app.repositories.base import MonitorRepository

class InMemoryMonitorRepository(MonitorRepository):
    def __init__(self) -> None:
        self._items: dict[int, Monitor] = {}
        self._next_id = 1

    def reset(self):
        self._items.clear()
        self._next_id = 1
        
    async def add(self, monitor: Monitor) -> Monitor:
        monitor.id = self._next_id
        self._items[monitor.id] = monitor
        self._next_id += 1
        return monitor
        
    async def get(self, monitor_id: int) -> Optional[Monitor]:
        return self._items.get(monitor_id)


    async def list_by_owner(self, owner_id: int) -> list[Monitor]:
        return [
            monitor
            for monitor in self._items.values()
            if monitor.owner_id == owner_id
        ]

    async def update(self, monitor: Monitor) -> Monitor:
        self._items[monitor.id] = monitor
        return monitor

    async def delete(self, monitor_id: int) -> bool:
        return self._items.pop(monitor_id, None) is not None

    
        



    
    