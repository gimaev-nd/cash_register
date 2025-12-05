from typing import cast

from cash_register.models import Game
from cash_register.types import BanknoteCount, GameDataV1, GameState, Nominal
from users.models import Gamer
from users.services.gamer import get_gamer

from .banknotes import DEFAULT_BANKNOTES, calc_cash


def get_game(gamer: Gamer) -> Game:
    if hasattr(gamer, "game"):
        game = cast(Game, gamer.game)
    else:
        game = Game.objects.create(gamer=gamer, data={}, version=1)
        init_game(game)
    return game


def get_game_by_gamer_name(name: str) -> Game:
    gamer = get_gamer(name)
    return get_game(gamer)


def init_game(game: Game):
    banknotes: list[BanknoteCount] = DEFAULT_BANKNOTES
    data: GameDataV1 = {
        "state": GameState.START,
        "buyer_number": 1,
        "buyer": {
            "number": 1,
            "product_cost": 80,
            "gave_money": 100,
            "got_money": 0,
        },
        "cash": calc_cash(banknotes),
        "cash_register": banknotes,
    }
    game.data = data
    game.save()


def start(game: Game):
    pass


def change_money(game: Game, nominal: Nominal):
    return


"""    game.data = data
    game.save()
"""
