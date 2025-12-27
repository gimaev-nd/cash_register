from operator import add, attrgetter, sub
from typing import Callable

from cash_register.types import BanknoteCount, Cash, CashSeq, Nominal

DEFAULT_BANKNOTES: Cash = [
    BanknoteCount(count=1, nominal=Nominal.THOUSAND),
    BanknoteCount(count=10, nominal=Nominal.FIVE_HUNDRED),
    BanknoteCount(count=10, nominal=Nominal.HUNDRED),
    BanknoteCount(count=10, nominal=Nominal.FIFTY),
    BanknoteCount(count=10, nominal=Nominal.TEN),
]


def sum_as_banknotes(value: int, max_nominal: Nominal | None = None) -> Cash:
    nominal_index = [*Nominal].index(max_nominal) + 1 if max_nominal else None
    nominals = sorted([*Nominal][:nominal_index], reverse=True)
    banknotes: Cash = []
    for nominal in nominals:
        count, value = divmod(value, nominal)
        if not count:
            continue
        banknotes.append(BanknoteCount(count=count, nominal=nominal))
    return sorted(banknotes, key=attrgetter("nominal"))


def change_banknotes(banknotes: Cash, nominal: Nominal) -> Cash:
    if not [*Nominal].index(nominal):
        return banknotes
    new_banknotes: Cash = [BanknoteCount(count=-1, nominal=nominal)]
    new_banknotes.extend(sum_as_banknotes(nominal, nominal.get_prev()))
    assert cash_sum(new_banknotes) == 0
    return cash_by_sum(banknotes, new_banknotes)


def merge_banknotes(
    banknotes_1: CashSeq,
    banknotes_2: CashSeq,
    operation: Callable[[int, int], int] = add,
) -> Cash:
    banknote_dict_1 = banknotes_as_dict(banknotes_1)
    banknote_dict_2 = banknotes_as_dict(banknotes_2)
    banknotes: Cash = []
    for nominal in Nominal:
        banknote_1 = banknote_dict_1.get(nominal)
        banknote_2 = banknote_dict_2.get(nominal)
        if banknote_1 and banknote_2:
            banknotes.append(
                BanknoteCount(
                    count=operation(banknote_1.count, banknote_2.count), nominal=nominal
                )
            )
        elif banknote_1:
            new_banknote_count = BanknoteCount(
                count=banknote_1.count, nominal=banknote_1.nominal
            )
            banknotes.append(new_banknote_count)
        elif banknote_2 and operation == sub:
            raise Exception("Неожиданое поведение", banknote_2, operation)
        elif banknote_2:
            new_banknote_count = BanknoteCount(
                count=banknote_2.count, nominal=banknote_2.nominal
            )
            banknotes.append(new_banknote_count)
    return banknotes


def cash_by_sum(cash_1: CashSeq, cash_2: CashSeq) -> Cash:
    return merge_banknotes(cash_1, cash_2, add)


def cash_difference(cash_1: CashSeq, cash_2: CashSeq) -> Cash:
    return merge_banknotes(cash_1, cash_2, sub)


def banknotes_as_dict(
    banknotes: CashSeq,
) -> dict[Nominal, BanknoteCount]:
    return {bn.nominal: bn for bn in banknotes if bn.count}


def cash_sum(banknotes: CashSeq) -> int:
    summ = 0
    for banknote in banknotes:
        summ += banknote.count * banknote.nominal
    return summ
