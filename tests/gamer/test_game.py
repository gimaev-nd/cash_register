import pytest

from cash_register.services.game import get_game
from users.models import Gamer
from users.services.gamer import get_gamer

pytestmark = pytest.mark.django_db


@pytest.fixture
def gamer() -> Gamer:
    return get_gamer("Вася")


def test_create_game(gamer):
    game = get_game(gamer)

    assert get_game(gamer) is not None
    assert game.gamer.name == "Вася"
