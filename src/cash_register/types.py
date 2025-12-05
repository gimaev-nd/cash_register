from typing import TypedDict
from typing_extensions import Sequence

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


class BuyerV1(TypedDict):
    number: int
    product_cost: int
    gave_money: int
    got_money: int


class BanknoteCount(TypedDict):
    count: int
    nominal: Nominal


class GameDataV1(TypedDict):
    state: GameState
    buyer_number: int
    buyer: BuyerV1
    cash: int  # остаток денег в кассе
    cash_register: Sequence[BanknoteCount]
