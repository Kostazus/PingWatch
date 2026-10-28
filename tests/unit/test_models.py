from datetime import datetime, timedelta, time, timezone
import pytest

from app.domain.models import CheckResult, Incident

NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

def test_check_result_rejects_naive_datetime():
    with pytest.raises(ValueError):
        CheckResult(
            monitor_id=1,
            ok=True,
            latency_ms=144,
            checked_at=datetime(2026, 1, 1, 12, 0)
        )

def test_is_slow_boundary():
    result = CheckResult(
        monitor_id=1,
        ok=True,
        latency_ms=500.0,
        checked_at=datetime.now(timezone.utc),
    )

    assert result.is_slow(500.0) is False

    result = CheckResult(
            monitor_id=1,
            ok=True,
            latency_ms=501.0,
            checked_at=datetime.now(timezone.utc),
        )

    assert result.is_slow(500.0) is True

def test_incident_duration():
    incident = Incident(
        id=1, 
        monitor_id=1,
        started_at=NOW,
        resolved_at=NOW + timedelta(minutes=5)
    )

    assert incident.duration == timedelta(minutes=5)

    open_incident = Incident(
        id=2,
        monitor_id=1,
        started_at=NOW,
    )

    assert open_incident.duration is None