from typing import cast

from cash_register.models import Game
from cash_register.services.products import all_products
from cash_register.types import (
    BanknoteCount,
    Cart,
    CartItem,
    CashRegisterState,
    ChangeState,
    GameDataV1,
    Nominal,
    PurchaseState,
    ScreenState,
)
from users.models import Gamer
from users.services.gamer import get_gamer

from .banknotes import DEFAULT_BANKNOTES, calc_cash, sum_as_banknotes


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
    product = all_products.get_random(1)[0]
    cart_Item: CartItem = {
        "product": product,
        "count": 1,
        "amount": product["price"],
    }
    cart: Cart = {
        "amount": cart_Item["amount"],
        "items": [cart_Item],
    }
    data: GameDataV1 = {
        "states": {
            "cash_register": CashRegisterState.START,
            "screen": ScreenState.START,
            "purchase": PurchaseState.START,
            "change": ChangeState.START,
        },
        "buyer_number": 1,
        "buyer": {
            "number": 1,
            "cart": cart,
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


def do_scan(game: Game):
    data = game.get_game_data()
    data["states"]["screen"] = ScreenState.AMOUNT
    data["states"]["purchase"] = PurchaseState.ASK_PAYMENT
    data["buyer"]["gave_money"] = data["buyer"]["cart"]["amount"]
    game.set_game_data(data)


def ask_payment(game: Game):
    data = game.get_game_data()
    data["states"]["purchase"] = PurchaseState.PAYMENT
    game.set_game_data(data)


def get_buyer_cash(game: Game) -> tuple[BanknoteCount, ...]:
    data = game.get_game_data()
    buyer = data["buyer"]
    return sum_as_banknotes(buyer["gave_money"])


def open_cash_register(game: Game):
    data = game.get_game_data()
    data["states"]["cash_register"] = CashRegisterState.OPEN
    game.set_game_data(data)


def noop(game: Game):
    pass
