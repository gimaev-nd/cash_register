import pytest

from cash_register.services.banknotes import (
    DEFAULT_BANKNOTES,
    calc_cash,
    change_banknotes,
    merge_banknotes,
    sum_as_banknotes,
)
from cash_register.types import BanknoteCount, Nominal


def test_nominal():
    assert Nominal.THOUSAND.get_prev() == Nominal.FIVE_HUNDRED


# @pytest.mark.skip("")
@pytest.mark.parametrize("nominal", [Nominal.THOUSAND])
def test_change(nominal: Nominal):
    banknotes_before: tuple[BanknoteCount, ...] = ({"count": 1, "nominal": nominal},)
    banknotes_after = change_banknotes(banknotes_before, nominal)
    assert calc_cash(banknotes_before) == calc_cash(banknotes_after)


def test_merge_banknotes():
    b1 = DEFAULT_BANKNOTES[2:]
    b2 = DEFAULT_BANKNOTES[:-2]
    banknotes = merge_banknotes(b1, b2)

    assert calc_cash(banknotes) == calc_cash(b1) + calc_cash(b2)


def test_sum_as_banknotes():
    assert sum_as_banknotes(2340) == (
        {"nominal": Nominal.TEN, "count": 4},
        {"nominal": Nominal.HUNDRED, "count": 1},
        {"nominal": Nominal.TWO_HUNDRED, "count": 1},
        {"nominal": Nominal.THOUSAND, "count": 2},
    )


def test_sum_as_banknotes_100():
    assert sum_as_banknotes(2340, Nominal.HUNDRED) == (
        {"nominal": Nominal.TEN, "count": 4},
        {"nominal": Nominal.HUNDRED, "count": 23},
    )
