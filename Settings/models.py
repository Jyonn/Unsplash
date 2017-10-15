from django.db import models


class Settings(models.Model):
    L = {
        'key': 32,
        'value': 512,
    }
    key = models.CharField(
        max_length=L['key'],
        unique=True,
    )
    value = models.CharField(
        max_length=L['value'],
    )

    @classmethod
    def create(cls, key, value):
        o = cls(key=key, value=value)
        try:
            o.save()
            return o
        except:
            return None

