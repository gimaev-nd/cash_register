from django.db import models

# Create your models here.


class Gamer(models.Model):
    name = models.CharField("Игрок", max_length=50)
