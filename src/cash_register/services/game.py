from typing import cast

from cash_register.models import Game
from cash_register.services.products import all_products
from cash_register.types import (
    BuyerV1,
    Cart,
    CartItem,
    CashRegister,
    CashRegisterState,
    CashType,
    Change,
    ChangeState,
    GameDataV1,
    Nominal,
    Purchase,
    PurchaseState,
    Screen,
    ScreenState,
)
from users.models import Gamer
from users.services.gamer import get_gamer

from .banknotes import DEFAULT_BANKNOTES, calc_cash, merge_banknotes, sum_as_banknotes


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
    banknotes = DEFAULT_BANKNOTES
    product = all_products.get_random(1)[0]
    cart_Item = CartItem(product=product, count=1, amount=product.price)
    cart = Cart(amount=cart_Item.amount, items=[cart_Item])
    data = GameDataV1(
        purchase=Purchase(state=PurchaseState.START, cash=[]),
        buyer=BuyerV1(number=1, cart=cart, gave_money=100, got_money=0, cash=[]),
        screen=Screen(state=ScreenState.START, product_cost=0, cash_amount=0, change=0),
        cash_register=CashRegister(
            state=CashRegisterState.START, cash=banknotes, amount=calc_cash(banknotes)
        ),
        change=Change(state=ChangeState.START, cash=[]),
    )
    game.set_game_data(data)


def start(game: Game):
    pass


def change_money(game: Game, nominal: Nominal):
    return


"""    game.data = data
    game.save()
"""


def do_scan(game: Game):
    data = game.get_game_data()
    data.purchase.state = PurchaseState.ASK_PAYMENT
    buyer = data.buyer
    buyer.gave_money = buyer.cart.amount
    screen = data.screen
    screen.state = ScreenState.COST
    screen.product_cost = buyer.cart.amount
    game.set_game_data(data)


def ask_payment(game: Game):
    data = game.get_game_data()
    data.purchase.state = PurchaseState.PAYMENT
    data.purchase.cash = get_buyer_cash(game)
    game.set_game_data(data)


def get_buyer_cash(game: Game) -> CashType:
    data = game.get_game_data()
    buyer = data.buyer
    return sum_as_banknotes(buyer.gave_money)


def open_cash_register(game: Game):
    data = game.get_game_data()
    data.cash_register.state = CashRegisterState.OPEN
    game.set_game_data(data)


def take_cashe(game: Game):
    data = game.get_game_data()
    data.purchase.state = PurchaseState.PAID
    data.cash_register.cash = merge_banknotes(
        data.cash_register.cash, data.purchase.cash
    )
    data.purchase.cash = []
    game.set_game_data(data)


def noop(game: Game):
    pass
