from datetime import datetime, timezone

from app.domain.models import User
from app.repositories.memory import InMemoryUserRepository


def make_user(email: str) -> User:
    return User(
        id=0,
        email=email,
        password_hash="hash",
        created_at=datetime.now(timezone.utc),
    )


async def test_add_assigns_incrementing_ids():
    repo = InMemoryUserRepository()

    saved1 = await repo.add(make_user(email="a@example.com"))
    assert saved1.id == 1

    saved2 = await repo.add(make_user(email="b@example.com"))
    assert saved2.id == 2


async def test_get_by_email():
    repo = InMemoryUserRepository()

    saved = await repo.add(make_user(email="a@example.com"))

    found = await repo.get_by_email("a@example.com")
    assert found == saved

    unknown = await repo.get_by_email("unknown@example.com")
    assert unknown is None


async def test_get_by_id():
    repo = InMemoryUserRepository()

    saved = await repo.add(make_user(email="a@example.com"))

    found = await repo.get(saved.id)
    missing = await repo.get(999)

    assert found == saved
    assert missing is None