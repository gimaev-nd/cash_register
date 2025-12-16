from collections.abc import Sequence
from typing import Any

from django.db.models.enums import IntegerChoices, TextChoices
from pydantic import BaseModel, field_validator, model_validator


class Nominal(IntegerChoices):
    TEN = 10
    FIFTY = 50
    HUNDRED = 100
    TWO_HUNDRED = 200
    FIVE_HUNDRED = 500
    THOUSAND = 1000

    def get_prev(self):
        nominals = [*Nominal]
        nominal_index = nominals.index(self)
        if nominal_index:
            return nominals[nominal_index - 1]


class CashRegisterState(TextChoices):
    START = "start", "Старт"
    OPEN = "open", "Открыто"
    CHANGE_MONEY = "change_money", "Размен"
    INCREASE = "increase", "Укрупнить"


class CashName(TextChoices):
    BUYER = "buyer", "Покупатель"
    PURCHASE = "purchase", "Оплата"
    CASH_REGISTER = "cash_register", "Касса"
    CHANGE = "change", "Сдача"


class ScreenState(TextChoices):
    START = "start", "Старт"
    COST = "cost", "Стоимость"
    CASH = "cash", "Наличные"


class PurchaseState(TextChoices):
    START = "start", "Старт"
    ASK_PAYMENT = "ask_payment", "Попросить оплату"
    PAYMENT = "payment", "Оплата"
    PAID = "paid", "Оплачено"


class ChangeState(TextChoices):
    START = "start", "Старт"


class Product(BaseModel):
    id: int
    name: str
    price: int

    @field_validator("price")
    def round_to_tens(cls, price: int):
        return ((price + 5) // 10) * 10


class CartItem(BaseModel):
    product: Product
    count: int
    amount: int


class Cart(BaseModel):
    amount: int
    items: list[CartItem]


class BanknoteCount(BaseModel):
    count: int
    nominal: Nominal


Cash = list[BanknoteCount]
CashSeq = Sequence[BanknoteCount]


class Buyer(BaseModel):
    number: int
    cart: Cart
    gave_money: int
    got_money: int
    cash: Cash


class Purchase(BaseModel):
    state: PurchaseState
    cash: Cash

    def reset_state(self):
        self.state = PurchaseState.START
        self.cash = []


class Screen(BaseModel):
    state: ScreenState
    product_cost: int
    cash_amount: int
    change: int

    def reset_state(self):
        self.state = ScreenState.START
        self.cash_amount = 0
        self.product_cost = 0
        self.change = 0


class CashRegister(BaseModel):
    state: CashRegisterState
    cash: Cash

    def reset_state(self):
        self.state = CashRegisterState.START

    @property
    def amount(self) -> int:
        from cash_register.services.banknotes import calc_cash

        return calc_cash(self.cash)


class Change(BaseModel):
    state: ChangeState
    cash: Cash

    def reset_state(self):
        self.state = ChangeState.START
        self.cash = []


class LevelConstrain(BaseModel):
    nominal: int
    random: bool
    count: int

    @model_validator(mode="before")
    @classmethod
    def validate_id(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        if isinstance(data, dict):
            data.setdefault("random", False)
            data.setdefault("count", 100)
        return data  # pyright: ignore[reportUnknownVariableType]


class Level(BaseModel):
    index: int
    name: str
    buyer_count: int
    max_cart_item_count: int
    constrains: list[LevelConstrain]

    @model_validator(mode="before")
    @classmethod
    def validate_id(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        if isinstance(data, dict):
            if "index" in data and data["index"] == "default":
                data["index"] = -1
        return data  # pyright: ignore[reportUnknownVariableType]

    def get_buyer(self, number: int):
        from cash_register.services.repositories.products import all_products

        cart_products = all_products.get_random(self.max_cart_item_count)
        items: list[CartItem] = []
        amount: int = 0
        for product in cart_products:
            cart_item = CartItem(product=product, count=1, amount=product.price)
            items.append(cart_item)
            amount += cart_item.amount
        cart = Cart(amount=amount, items=items)
        return Buyer(number=number, cart=cart, gave_money=100, got_money=0, cash=[])


class LevelHistory(BaseModel):
    level: Level
    buyers: list[Buyer]

    def get_buyer(self):
        number = len(self.buyers) + 1
        return self.level.get_buyer(number)


class GameData(BaseModel):
    buyer: Buyer
    screen: Screen
    purchase: Purchase
    cash_register: CashRegister
    change: Change
    level_history: LevelHistory
    history: list[LevelHistory]

    def reset_state(self):
        self.screen.reset_state()
        self.purchase.reset_state()
        self.cash_register.reset_state()
        self.change.reset_state()

    def new_level(self):
        pass
