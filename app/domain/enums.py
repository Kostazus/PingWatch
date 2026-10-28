from enum import StrEnum

class Role(StrEnum):
    USER = 'user'
    ADMIN = "admin"

class MonitorStatus(StrEnum):
    UP = "up"
    DOWN = "down"
    UNKNOWN = "unknown"
    PAUSED = "paused"

class IncidentStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"



