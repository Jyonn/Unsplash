""" Adel Liu 180111

系统配置类
"""
from django.db import models


class Config(models.Model):
    """
    系统配置，如七牛密钥等
    """
    L = {
        'key': 512,
        'value': 1024,
    }
    key = models.CharField(
        max_length=L['key'],
    )
    value = models.CharField(
        max_length=L['value'],
    )
