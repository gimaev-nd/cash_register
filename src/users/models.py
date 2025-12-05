from django.db import models


# Create your models here.
#
class Gamer(models.Model):
    name: str = models.CharField("Игрок", max_length=50)  # pyright: ignore[reportUnknownVariableType, reportAssignmentType]
