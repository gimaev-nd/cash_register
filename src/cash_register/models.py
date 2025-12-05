from typing import cast

from django.db import models

from cash_register.types import GameDataV1


def parse(game):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    return cast(GameDataV1, game)


class Game(models.Model):
    gamer = models.OneToOneField(
        "users.Gamer", models.CASCADE, related_name="game", verbose_name="Игрок"
    )
    data = models.JSONField("Данные игры")
    version = models.IntegerField("Версия схемы сотояния игры")

    def get_game_data(self) -> GameDataV1:
        self.update_version()
        return parse(self.data)  # pyright: ignore[reportAny]

    def update_version(self) -> None:
        pass
