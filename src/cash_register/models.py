from django.db import models

from cash_register.types import GameData


class Game(models.Model):
    gamer = models.OneToOneField(
        "users.Gamer", models.CASCADE, related_name="game", verbose_name="Игрок"
    )
    data = models.JSONField("Данные игры")

    def get_game_data(self) -> GameData:
        return GameData.model_validate(self.data)

    def set_game_data(self, data: GameData) -> None:
        self.data = data.model_dump()
        self.save()
