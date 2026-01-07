from django.db import models


# Create your models here.
#
class Gamer(models.Model):
    name = models.CharField("Игрок", max_length=50)
    code = models.IntegerField("Табельный номер", null=True)

    def save(self, force_insert=False, **kwargs):
        super().save(force_insert=force_insert, **kwargs)
        if not self.code:
            self.refresh_from_db()
            self.code = (self.pk * 3357_913) % 9_000_000 + 1_000_000
            self.save(**kwargs)
