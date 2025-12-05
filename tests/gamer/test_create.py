import pytest, sys

from users.services.gamer import create_gamer

pytestmark = pytest.mark.django_db

def test_create_new_gamer():
    gamer = create_gamer("Маша")

    assert gamer.name == "Маша"


def test_create_exist_gamer():
    gamer = create_gamer("Маша")
    gamer2 = create_gamer("Маша")

    assert gamer.pk == gamer2.pk
