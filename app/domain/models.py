from dataclasses import dataclass
from datetime import datetime, timedelta

from app.domain.enums import IncidentStatus, MonitorStatus, Role

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    created_at: datetime
    role: Role = Role.USER
    is_active: bool = True

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")

@dataclass
class Monitor:
    id: int
    owner_id: int
    name: str
    url: str
    created_at: datetime
    method: str = "GET"
    interval_seconds: int = 60
    timeout_seconds: int = 10
    expected_status: int = 200
    status: MonitorStatus = MonitorStatus.UNKNOWN

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")


@dataclass
class CheckResult:
    monitor_id: int
    checked_at: datetime
    ok: bool
    latency_ms: float
    status_code: int | None = None
    error: str | None = None

    def __post_init__(self) -> None:
        if self.checked_at.tzinfo is None or self.checked_at.utcoffset() is None:
            raise ValueError("checked_at must be timezone-aware")

    def is_slow(self, threshold_ms: float) -> bool:
        return self.latency_ms > threshold_ms

@dataclass
class Incident:
    id: int
    monitor_id: int
    started_at: datetime
    resolved_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.started_at.tzinfo is None or self.started_at.utcoffset() is None:
            raise ValueError("started_at must be timezone-aware")

        if self.resolved_at is not None and (
            self.resolved_at.tzinfo is None or self.resolved_at.utcoffset() is None
        ):
            raise ValueError("resolved_at must be timezone-aware")

        if self.resolved_at is not None and self.resolved_at < self.started_at:
            raise ValueError("resolved_at cannot be earlier than started_at")

    @property
    def duration(self) -> timedelta | None:
        if self.resolved_at is None:
            return None

        return self.resolved_at - self.started_at

    @property
    def status(self) -> IncidentStatus:
        if self.resolved_at is None:
            return IncidentStatus.OPEN

        return IncidentStatus.RESOLVED

    
    