import pytest

from cash_register.services.banknotes import (
    DEFAULT_BANKNOTES,
    cash_sum,
    change_banknotes,
    merge_banknotes,
    sum_as_banknotes,
)
from cash_register.types import BanknoteCount, Cash, Nominal


def test_nominal():
    assert Nominal.THOUSAND.get_prev() == Nominal.FIVE_HUNDRED


# @pytest.mark.skip("")
@pytest.mark.parametrize("nominal", [Nominal.THOUSAND])
def test_change(nominal: Nominal):
    banknotes_before: Cash = [BanknoteCount(count=1, nominal=nominal)]
    banknotes_after = change_banknotes(banknotes_before, nominal)
    assert cash_sum(banknotes_before) == cash_sum(banknotes_after)


def test_merge_banknotes():
    b1 = DEFAULT_BANKNOTES[2:]
    b2 = DEFAULT_BANKNOTES[:-2]
    banknotes = merge_banknotes(b1, b2)

    assert cash_sum(banknotes) == cash_sum(b1) + cash_sum(b2)


def test_sum_as_banknotes():
    assert sum_as_banknotes(2340) == [
        BanknoteCount(nominal=Nominal.TEN, count=4),
        BanknoteCount(nominal=Nominal.HUNDRED, count=1),
        BanknoteCount(nominal=Nominal.TWO_HUNDRED, count=1),
        BanknoteCount(nominal=Nominal.THOUSAND, count=2),
    ]


def test_sum_as_banknotes_100():
    assert sum_as_banknotes(2340, Nominal.HUNDRED) == [
        BanknoteCount(nominal=Nominal.TEN, count=4),
        BanknoteCount(nominal=Nominal.HUNDRED, count=23),
    ]
