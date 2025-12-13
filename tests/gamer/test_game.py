import pytest

from cash_register.models import Game
from cash_register.services.game import get_game, get_game_by_gamer_name
from users.models import Gamer
from users.services.gamer import get_gamer

pytestmark = pytest.mark.django_db


@pytest.fixture
def gamer() -> Gamer:
    return get_gamer("Вася")


@pytest.fixture
def game(gamer) -> Game:
    return get_game(gamer)


def test_create_game(gamer):
    game = get_game(gamer)

    assert get_game(gamer) is not None
    assert game.gamer.name == "Вася"


def test_success_get_game_by_gamer_name(game):
    given_game = get_game_by_gamer_name("Вася")

    assert given_game.gamer.name == "Вася"
    assert given_game == game


def test_success_create_get_game_by_gamer_name():
    game = get_game_by_gamer_name("Вася")

    assert game.gamer.name == "Вася"


@pytest.mark.usefixtures("game")
def test_fail_create_get_game_by_gamer_name():
    game = get_game_by_gamer_name("Петя")

    assert game.gamer.name != "Вася"
