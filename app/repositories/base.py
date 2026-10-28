from typing import Protocol, Optional
from app.domain.models import Monitor, User


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

class UserRepository(Protocol):
    async def add(self, user: User) -> User:
        ...

    async def get(self, user_id: int) -> Optional[User]:
        ...

    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    async def update(self, user: User) -> User:
        ...

    
