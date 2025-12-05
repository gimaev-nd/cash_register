import pytest

from users.services.gamer import get_gamer

pytestmark = pytest.mark.django_db


def test_create_new_gamer():
    gamer = get_gamer("Маша")

    assert gamer.name == "Маша"


def test_create_exist_gamer():
    gamer = get_gamer("Маша")
    gamer2 = get_gamer("Маша")

    assert gamer.id == gamer2.id  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
