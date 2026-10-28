from app.domain.models import CheckResult, Incident
from typing import Optional

class IncidentTracker:

    def __init__(self, monitor_id: int, failure_threshold: int = 3) -> None:
        if failure_threshold < 1:
            raise ValueError("failure_threshold must be at least 1")
        self.monitor_id = monitor_id
        self.failure_threshold = failure_threshold
        self._consecutive_failures = 0
        self._open_incident: Optional[Incident] = None
        self._next_id = 1

    def process(self, result: CheckResult) -> Optional[Incident]:
        if result.ok:
            return self._handle_success(result)
        return self._handle_failure(result)

    def _handle_success(self, result: CheckResult) -> Optional[Incident]:
        self._consecutive_failures = 0
        if self._open_incident is None:
            return None
        incident = self._open_incident
        incident.resolved_at = result.checked_at
        self._open_incident = None
        return incident

    def _handle_failure(self, result: CheckResult) -> Optional[Incident]:
        if self._open_incident is not None:
            return None
        self._consecutive_failures += 1
        if self._consecutive_failures < self.failure_threshold:
            return None
        incident = Incident(
            id=self._next_id,
            monitor_id=self.monitor_id,
            started_at=result.checked_at,
        )
        self._next_id += 1
        self._open_incident = incident
        return incident

    
