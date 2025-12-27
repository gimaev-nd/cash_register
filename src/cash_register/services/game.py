from typing import Callable, cast

from cash_register.models import Game
from cash_register.services.repositories.levels import levels
from cash_register.services.repositories.products import all_products
from cash_register.types import (
    BanknoteCount,
    Buyer,
    Cart,
    CartItem,
    Cash,
    CashName,
    CashRegister,
    CashRegisterState,
    CashState,
    Change,
    ChangeState,
    GameData,
    LevelHistory,
    Nominal,
    Purchase,
    PurchaseState,
    Screen,
    ScreenState,
)
from users.models import Gamer
from users.services.gamer import get_gamer

from .banknotes import (
    DEFAULT_BANKNOTES,
    cash_by_sum,
    cash_difference,
    cash_sum,
    sum_as_banknotes,
)


def get_game(gamer: Gamer) -> Game:
    if hasattr(gamer, "game"):
        game = cast(Game, gamer.game)  # pyright: ignore[reportAttributeAccessIssue]
    else:
        game = Game.objects.create(gamer=gamer, data={})
        init_game(game)
    return game


def get_game_by_gamer_name(name: str) -> Game:
    gamer = get_gamer(name)
    return get_game(gamer)


def init_game(game: Game):
    banknotes = DEFAULT_BANKNOTES.copy()
    product = all_products.get_random(1)[0]
    cart_Item = CartItem(product=product, count=1, amount=product.price)
    cart = Cart(amount=cart_Item.amount, items=[cart_Item])
    data = GameData(
        purchase=Purchase(state=PurchaseState.START, cash_state=CashState()),
        buyer=Buyer(number=1, cart=cart, gave_money=100, got_money=0, cash=[]),
        screen=Screen(state=ScreenState.START, product_cost=0, cash_amount=0, change=0),
        cash_register=CashRegister(
            state=CashRegisterState.START, cash_state=CashState(cash=banknotes)
        ),
        change=Change(state=ChangeState.START, cash_state=CashState()),
        level_history=LevelHistory(level=levels.get(), buyers=[]),
        history=[],
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
    data.purchase.cash_state.cash = get_buyer_cash(game)
    game.set_game_data(data)


def get_buyer_cash(game: Game) -> Cash:
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
    data.cash_register.cash_state.cash = cash_by_sum(
        data.cash_register.cash_state.cash, data.purchase.cash_state.cash
    )
    data.screen.state = ScreenState.CASH
    data.screen.cash_amount = cash_sum(data.purchase.cash_state.cash)
    data.screen.change = data.screen.cash_amount - data.screen.product_cost
    data.purchase.cash_state.reset()
    game.set_game_data(data)


def reset_state(game: Game):
    data = game.get_game_data()
    data.reset_state()
    game.set_game_data(data)


def check(game: Game):
    data = game.get_game_data()
    data.buyer.got_money = cash_sum(data.change.cash_state.cash)
    data.change.cash_state.reset()
    data.level_history.buyers.append(data.buyer)
    level = data.level_history.level
    if level.buyer_count == data.buyer:
        data.new_level()
    else:
        data.buyer = data.level_history.get_buyer()
    data.reset_state()
    game.set_game_data(data)


def get_cash_state(game_data: GameData, cash_name: CashName) -> CashState:
    if cash_name == CashName.PURCHASE:
        return game_data.purchase.cash_state
    if cash_name == CashName.CASH_REGISTER:
        return game_data.cash_register.cash_state
    if cash_name == CashName.CHANGE:
        return game_data.change.cash_state
    raise Exception("Неожиданое поведение", game_data, cash_name)


def get_cash(game_data: GameData, cash_name: CashName) -> Cash:
    if cash_name in (CashName.PURCHASE, CashName.CASH_REGISTER, CashName.CHANGE):
        return get_cash_state(game_data, cash_name).cash
    if cash_name == CashName.BUYER:
        return game_data.buyer.cash
    raise Exception("Неожиданое поведение", game_data, cash_name)


def _move_cash(cash: Cash, delta_cash: Cash, action: Callable):
    changed_cash = action(cash, delta_cash)
    cash.clear()
    cash.extend(x for x in changed_cash if x.count)


def move_cash(
    game: Game,
    cash_name_src: CashName,
    cash_name_dst: CashName,
    nominal: Nominal,
    count: int = 1,
) -> None:
    data = game.get_game_data()
    cash_src = get_cash(data, cash_name_src)
    cash_dst = get_cash(data, cash_name_dst)
    delta_cash = [BanknoteCount(nominal=nominal, count=count)]
    _move_cash(cash_src, delta_cash, cash_difference)
    _move_cash(cash_dst, delta_cash, cash_by_sum)
    game.set_game_data(data)


def new_level(game: Game):
    pass


def noop(game: Game):
    pass
