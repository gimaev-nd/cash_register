from collections.abc import Sequence
from operator import itemgetter

from cash_register.types import BanknoteCount, Nominal

DEFAULT_BANKNOTES: list[BanknoteCount] = [
    {"count": 1, "nominal": Nominal.THOUSAND},
    {"count": 10, "nominal": Nominal.FIVE_HUNDRED},
    {"count": 10, "nominal": Nominal.HUNDRED},
    {"count": 10, "nominal": Nominal.FIFTY},
    {"count": 10, "nominal": Nominal.TEN},
]


def sum_as_banknotes(value: int, max_nominal: Nominal = None) -> tuple[BanknoteCount,...]:
    nominal_index = [*Nominal].index(max_nominal) + 1 if max_nominal else None
    nominals = sorted([*Nominal][:nominal_index], reverse=True)
    banknotes: list[BanknoteCount] = []
    for nominal in nominals:
        count, value = divmod(value, nominal)
        if not count:
            continue
        banknotes.append({"count": count, "nominal": nominal})
    return tuple(sorted(banknotes, key=itemgetter("nominal")))


def change_banknotes(
    banknotes: tuple[BanknoteCount], nominal: Nominal
) -> tuple[BanknoteCount]:
    if not [*Nominal].index(nominal):
        return banknotes
    new_banknotes = [{"count": -1, "nominal": nominal}]
    new_banknotes.extend(sum_as_banknotes(nominal, nominal.get_prev()))
    assert calc_cash(new_banknotes) == 0
    return merge_banknotes(banknotes, new_banknotes)


def merge_banknotes(
    banknotes_1: Sequence[BanknoteCount], banknotes_2: Sequence[BanknoteCount]
) -> tuple[BanknoteCount,...]:
    banknote_dict_1 = banknotes_as_dict(banknotes_1)
    banknote_dict_2 = banknotes_as_dict(banknotes_2)
    banknotes: list[BanknoteCount] = []
    for nominal in Nominal:
        banknote_1 = banknote_dict_1.get(nominal)
        banknote_2 = banknote_dict_2.get(nominal)
        if banknote_1 and banknote_2:
            banknotes.append(
                {"nominal": nominal, "count": banknote_1["count"] + banknote_2["count"]}
            )
        elif banknote_1:
            banknotes.append(banknote_1)
        elif banknote_2:
            banknotes.append(banknote_2)
    return tuple(banknotes)


def banknotes_as_dict(
    banknotes: Sequence[BanknoteCount],
) -> dict[Nominal, BanknoteCount]:
    return {bn["nominal"]: bn for bn in banknotes if bn["count"]}


def calc_cash(banknotes: Sequence[BanknoteCount]) -> int:
    summ = 0
    for banknote in banknotes:
        summ += banknote["count"] * banknote["nominal"]
    return summ
