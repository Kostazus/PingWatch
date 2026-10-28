from datetime import datetime, timedelta, timezone

import pytest

from app.domain.enums import IncidentStatus
from app.domain.incident_tracker import IncidentTracker
from app.domain.models import CheckResult
from app.repositories.memory import InMemoryMonitorRepository

BASE = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)


def make_result(ok: bool, minute: int) -> CheckResult:
    return CheckResult(
        monitor_id=1,
        checked_at=BASE + timedelta(minutes=minute),
        ok=ok,
        latency_ms=100.0,
        status_code=200 if ok else 500,
    )


def feed(tracker: IncidentTracker, oks: list) -> list:
    """Подаёт результаты по одному в минуту, возвращает все изменения."""
    changes = []
    for minute, ok in enumerate(oks):
        change = tracker.process(make_result(ok, minute))
        if change is not None:
            changes.append(change)
    return changes


@pytest.mark.parametrize("oks, expected_changes", [
    ([False, False], 0),                          # две неудачи: рано
    ([False, False, False], 1),                   # третья открывает
    ([False, False, True, False, False], 0),      # успех сбросил серию
    ([False] * 10, 1),                            # длинный сбой: один инцидент
])
def test_incident_opening(oks, expected_changes):
    tracker = IncidentTracker(monitor_id=1)
    changes = feed(tracker, oks)
    assert len(changes) == expected_changes


def test_success_resolves_incident():
    tracker = IncidentTracker(monitor_id=1)
    changes = feed(tracker, [False, False, False, True])

    assert len(changes) == 2                      # открыт, затем закрыт
    assert changes[0] is changes[1]               # это один и тот же объект
    incident = changes[0]
    assert incident.status == IncidentStatus.RESOLVED
    assert incident.duration == timedelta(minutes=1)   # с 3-й минуты (2) до 4-й (3)


def test_new_incident_after_resolution():
    tracker = IncidentTracker(monitor_id=1)
    changes = feed(tracker, [False, False, False, True, False, False, False])

    assert len(changes) == 3                      # открыт, закрыт, открыт новый
    first, new = changes[0], changes[2]
    assert new is not first
    assert new.id == 2
    assert new.status == IncidentStatus.OPEN


def test_invalid_threshold():
    with pytest.raises(ValueError):
        IncidentTracker(monitor_id=1, failure_threshold=0)

