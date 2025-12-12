from functools import cached_property
from pathlib import Path

import ruyaml
from django.conf import settings

from cash_register.types import Level

yaml = ruyaml.YAML()


class Levels:
    def __init__(self, levels: list[Level]) -> None:
        self._levels: list[Level] = levels
        self._current_level_index: int = 0

    def get(self, level_id: int | None = None) -> Level:
        self._current_level_index = level_id or 1
        level = self.map.get(self._current_level_index) or self.map[-1]
        self._current_level_index = level.index
        return level

    def get_next(self) -> Level:
        if self._current_level_index == -1:
            return self.get(-1)
        return self.get(self._current_level_index + 1)

    @classmethod
    def load(cls, levels_file: Path | str) -> "Levels":
        if isinstance(levels_file, str):
            levels_file = Path(levels_file)
        with levels_file.open("r") as f:
            level_list = yaml.load(f)  # type: ignore
            levels = [Level.model_validate(level) for level in level_list["levels"]]
        return Levels(levels)

    @cached_property
    def map(self) -> dict[int, Level]:
        result: dict[int, Level] = {}
        for level in self._levels:
            result[level.index] = level
        return result


levels = Levels.load(settings.CASH_REGISTER_DATA_DIR / "levels.yaml")
