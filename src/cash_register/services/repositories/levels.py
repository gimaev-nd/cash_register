from functools import cached_property
from pathlib import Path

import ruyaml
from django.conf import settings

from cash_register.types import Level

yaml = ruyaml.YAML()


class Levels:
    def __init__(self, levels: list[Level]) -> None:
        self._levels: list[Level] = levels

    def get(self, level_id: int) -> Level:
        return self.map[level_id]

    @classmethod
    def load(cls, levels_file: Path | str) -> "Levels":
        if isinstance(levels_file, str):
            levels_file = Path(levels_file)
        with levels_file.open("r") as f:
            level_list: list[Level] = yaml.load(f)  # type: ignore
            levels = [Level.model_validate(p) for p in level_list]
        return Levels(levels)

    @cached_property
    def map(self) -> dict[int, Level]:
        result: dict[int, Level] = {}
        for level in self._levels:
            result[level.id] = level
        return result


levels = Levels.load(settings.CASH_REGISTER_DATA_DIR / "levels.yaml")
