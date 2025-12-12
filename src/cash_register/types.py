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


CashType = list[BanknoteCount]


class BuyerV1(BaseModel):
    number: int
    cart: Cart
    gave_money: int
    got_money: int
    cash: CashType


class Purchase(BaseModel):
    state: PurchaseState
    cash: CashType


class Screen(BaseModel):
    state: ScreenState
    product_cost: int
    cash_amount: int
    change: int


class CashRegister(BaseModel):
    state: CashRegisterState
    cash: CashType
    amount: int


class Change(BaseModel):
    state: ChangeState
    cash: CashType


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
    buyers: int
    max_cart_item_count: int
    constrains: list[LevelConstrain]

    @model_validator(mode="before")
    @classmethod
    def validate_id(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        if isinstance(data, dict):
            if "index" in data and data["index"] == "default":
                data["index"] = -1
        return data  # pyright: ignore[reportUnknownVariableType]


class LevelHistory(BaseModel):
    level: Level
    buyers: list[BuyerV1]


class GameDataV1(BaseModel):
    buyer: BuyerV1
    screen: Screen
    purchase: Purchase
    cash_register: CashRegister
    change: Change
    level: Level
    history: list[LevelHistory]
