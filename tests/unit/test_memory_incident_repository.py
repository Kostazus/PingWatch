from datetime import datetime, timezone, timedelta

from app.domain.models import Incident
from app.repositories.memory import InMemoryIncidentRepository

NOW = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

def make_incident(monitor_id) -> Incident:
    return Incident(
        id=0,
        monitor_id=monitor_id,
        started_at=NOW
    )

async def test_add_assigns_incrementing_ids():
    repo = InMemoryIncidentRepository()

    incident1 = make_incident(monitor_id=1)
    incident2 = make_incident(monitor_id=2)

    saved1 = await repo.add(incident1)
    assert incident1 == saved1

    saved2 = await repo.add(incident2)
    assert incident2 == saved2

async def test_get_open_for_monitor():
    repo = InMemoryIncidentRepository()

    incident = make_incident(monitor_id=1)
    saved = await repo.add(incident)

    found = await repo.get_open_for_monitor(1)
    assert found == saved

    found1 = await repo.get_open_for_monitor(2)
    assert found1 is None

    saved.resolved_at = NOW + timedelta(minutes=5)
    saved = await repo.update(saved)

    found = await repo.get_open_for_monitor(1)
    assert found is None

async def test_list_for_monitor():
    repo = InMemoryIncidentRepository()

    incident1 = make_incident(monitor_id=1)
    incident2 = make_incident(monitor_id=2)
    incident3 = make_incident(monitor_id=1)

    saved1 = await repo.add(incident1)
    saved2 = await repo.add(incident2)
    saved3 = await repo.add(incident3)
    

    found = await repo.list_for_monitor(1)
    assert len(found) == 2



    


