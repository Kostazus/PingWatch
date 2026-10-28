from datetime import datetime, timezone

from app.domain.models import Monitor
from app.repositories.memory import InMemoryMonitorRepository


def make_monitor(owner_id: int) -> Monitor:
    return Monitor(
        id=0,
        owner_id=owner_id,
        name="Correct",
        url='https://example.com',
        created_at=datetime.now(timezone.utc),
    )


async def test_add_assigns_incrementing_ids():
    repo = InMemoryMonitorRepository()

    monitor1 = make_monitor(owner_id=1)
    monitor2 = make_monitor(owner_id=2)

    saved1 = await repo.add(monitor1)
    assert saved1.id == 1

    saved2 = await repo.add(monitor2)
    assert saved2.id == 2


async def test_get_returns_monitor_or_none():
    repo = InMemoryMonitorRepository()

    monitor = make_monitor(owner_id=1)
    saved = await repo.add(monitor)

    found = await repo.get(saved.id)
    missing = await repo.get(999)

    assert found == saved
    assert missing is None


async def test_list_by_owner_returns_only_owner_monitors():
    repo = InMemoryMonitorRepository()

    await repo.add(make_monitor(owner_id=1))
    await repo.add(make_monitor(owner_id=2))
    await repo.add(make_monitor(owner_id=1))

    monitors = await repo.list_by_owner(owner_id=1)

    assert len(monitors) == 2
    assert all(monitor.owner_id == 1 for monitor in monitors)


async def test_delete_returns_true_or_false():
    repo = InMemoryMonitorRepository()

    monitor = make_monitor(owner_id=1)
    saved = await repo.add(monitor)

    delete_result = await repo.delete(saved.id)
    assert delete_result is True

    assert await repo.get(saved.id) is None

    non_existent_delete_result = await repo.delete(999)
    assert non_existent_delete_result is False