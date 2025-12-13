from django.db import models

from cash_register.types import GameDataV1


class Game(models.Model):
    gamer = models.OneToOneField(
        "users.Gamer", models.CASCADE, related_name="game", verbose_name="Игрок"
    )
    data = models.JSONField("Данные игры")

    def get_game_data(self) -> GameDataV1:
        return GameDataV1.model_validate(self.data)

    def set_game_data(self, data: GameDataV1) -> None:
        self.data = data.model_dump()
        self.save()
