from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from random import randint, shuffle
from typing import TypedDict

from django.db.models.enums import IntegerChoices, TextChoices


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


class GameState(TextChoices):
    START = "Start", "Старт"


class ScreenState(TextChoices):
    START = "start", "Старт"
    AMOUNT = "amount", "Сумма"


class Product(TypedDict):
    id: int
    name: str
    price: int


class CartItem(TypedDict):
    product: Product
    count: int
    amount: int


@dataclass
class Products:
    products: list[Product]

    def get(self, id: int) -> Product:
        product = self.products[id]
        return {
            "id": product["id"],
            "name": product["name"],
            "price": int(round(product["price"], -1)),
        }

    def get_random(self, count: int | None = None) -> list[Product]:
        _count: int = count or randint(1, 8)
        product_ids: set[int] = set()
        products: list[Product] = []
        while len(product_ids) < _count:
            product_id = randint(0, self.count - 1)
            if product_id in product_ids:
                continue
            product_ids.add(product_id)
            products.append(self.get(product_id))
        shuffle(products)
        return products

    @cached_property
    def count(self):
        return len(self.products)

    @cached_property
    def map(self) -> dict[int, Product]:
        return {p["id"]: p for p in self.products}


class Cart(TypedDict):
    amount: int
    items: list[CartItem]


class BuyerV1(TypedDict):
    number: int
    cart: Cart
    gave_money: int
    got_money: int


class BanknoteCount(TypedDict):
    count: int
    nominal: Nominal


class GameStates(TypedDict):
    game: GameState
    screen: ScreenState


class GameDataV1(TypedDict):
    states: GameStates
    buyer_number: int
    buyer: BuyerV1
    cash: int  # остаток денег в кассе
    cash_register: Sequence[BanknoteCount]
