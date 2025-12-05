from pyexpat import model
from tkinter import N
from turtle import mode
from typing import Any, TypedDict, cast

from django.db import models


class GameDataV1(TypedDict):
    pass


def parse(game):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    return cast(GameDataV1, game)


class Game(models.Model):
    gamer = models.ForeignKey(
        "users.Gamer", models.CASCADE, "games", verbose_name="Игрок"
    )
    game = models.JSONField("Данные игры")
    version = models.IntegerField("Версия схемы сотояния игры")

    def get_game_data(self) -> GameDataV1:
        self.update_version()
        return parse(self.game)  # pyright: ignore[reportAny]

    def update_version(self) -> None:
        pass
