import pytest

from cash_register.models import Game
from cash_register.services.game import get_game
from users.models import Gamer
from users.services.gamer import get_gamer


@pytest.fixture
def gamer() -> Gamer:
    return get_gamer("Вася")


@pytest.fixture
def game(gamer: Gamer) -> Game:
    return get_game(gamer)
