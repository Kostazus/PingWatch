from typing import Optional

from app.domain.models import Monitor, User, Incident
from app.repositories.base import MonitorRepository, UserRepository, IncidentRepository


class InMemoryMonitorRepository(MonitorRepository):
    def __init__(self) -> None:
        self._items: dict[int, Monitor] = {}
        self._next_id = 1

    def reset(self) -> None:
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


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._items: dict[int, User] = {}
        self._next_id = 1

    def reset(self) -> None:
        self._items.clear()
        self._next_id = 1

    async def add(self, user: User) -> User:
        user.id = self._next_id
        self._items[user.id] = user
        self._next_id += 1
        return user

    async def get(self, user_id: int) -> Optional[User]:
        return self._items.get(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        for user in self._items.values():
            if user.email == email:
                return user
        return None

    async def update(self, user: User) -> User:
        self._items[user.id] = user
        return user

class InMemoryIncidentRepository(IncidentRepository):
    def __init__(self) -> None:
        self._items: dict[int, Incident] = {}
        self._next_id = 1

    def reset(self):
        self._items.clear()
        self._next_id = 1

    async def add(self, incident: Incident):
        incident_id = self._next_id
        self._items[incident_id] = incident
        self._next_id += 1
        return incident

    async def get(self, incident_id: int):
        return self._items.get(incident_id)

    async def get_open_for_monitor(self, monitor_id: int):
        for incident in self._items.values():
            if incident.monitor_id == monitor_id and incident.resolved_at is None:
                return incident

        return None

    async def update(self, incident):
        self._items[incident.id] = incident
        return incident

    async def list_for_monitor(self, monitor_id: int):
        incidents = []

        for incident in self._items.values():
            if incident.monitor_id == monitor_id:
                incidents.append(incident)
        return sorted(incidents, key=lambda incident: incident.id)
        
        