""" Adel Liu 180111

系统配置类
"""
from SmartDjango import models, E


@E.register(id_processor=E.idp_cls_prefix())
class ConfigError:
    CREATE_CONFIG = E("更新配置错误")
    CONFIG_NOT_FOUND = E("不存在的配置")


class Config(models.Model):
    """
    系统配置，如七牛密钥等
    """
    key = models.CharField(
        max_length=512,
        unique=True,
    )
    value = models.CharField(
        max_length=1024,
    )

    @classmethod
    def get_config_by_key(cls, key):
        cls.validator(locals())

        try:
            config = cls.objects.get(key=key)
        except cls.DoesNotExist as err:
            raise ConfigError.CONFIG_NOT_FOUND(debug_message=err)

        return config

    @classmethod
    def get_value_by_key(cls, key, default=None):
        try:
            config = cls.get_config_by_key(key)
            return config.value
        except Exception:
            return default

    @classmethod
    def update_value(cls, key, value):
        cls.validator(locals())

        try:
            config = cls.get_config_by_key(key)
            config.value = value
            config.save()
        except E as e:
            if e.eis(ConfigError.CONFIG_NOT_FOUND):
                try:
                    config = cls(
                        key=key,
                        value=value,
                    )
                    config.save()
                except Exception as err:
                    raise ConfigError.CREATE_CONFIG(debug_message=err)
            else:
                raise e
        except Exception as err:
            raise ConfigError.CREATE_CONFIG(debug_message=err)


class ConfigInstance:
    UNSPLASH_CLIENT_ID = 'unsplash-client-id'
    UNSPLASH_SECRET = 'unsplash-secret'
    UNSPLASH_REDIRECT_URI = 'unsplash-redirect-uri'
    UNSPLASH_HOST = 'https://unsplash.com'
    UNSPLASH_API_HOST = "https://api.unsplash.com"
    LAST_CLEAR_TIME = 'last-clear-time'


CI = ConfigInstance
