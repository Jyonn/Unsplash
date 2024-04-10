from SmartDjango import models, E, Hc

from Base.api import UnsplashAPI
from Photo.models import Photo


@E.register(id_processor=E.idp_cls_prefix())
class UserError:
    CREATE = E("创建用户失败", hc=Hc.InternalServerError)
    NO_LEGAL_USER = E("没有合法用户", hc=Hc.ServiceUnavailable)


class User(models.Model):
    user_id = models.CharField(
        max_length=20,
        primary_key=True,
    )
    username = models.CharField(
        max_length=20,
        unique=True,
    )
    access_token = models.CharField(
        max_length=64,
    )
    expired = models.BooleanField(
        default=False,
    )
    email = models.EmailField(
        default=None,
        blank=True,
        null=True,
    )

    @classmethod
    def create(cls, access_token):
        profile = UnsplashAPI.get_user_profile(access_token)
        user_id = profile.get('id')
        username = profile.get('username')
        email = profile.get('email')

        try:
            user = cls.objects.get(pk=user_id)
            user.username = username
            user.email = email
            user.access_token = access_token
            user.expired = False
        except Exception as _:
            user = cls(
                user_id=user_id,
                username=username,
                access_token=access_token,
                email=email,
                expired=False,
            )

        try:
            user.save()
        except Exception as _:
            raise UserError.CREATE

        return user

    @classmethod
    def get_photo(cls):
        for user in cls.objects.filter(expired=False):
            photo = UnsplashAPI.get_random_photo(user.access_token)
            if photo is None:
                return Photo.get_random_photo()
            Photo.clear()
            photo = Photo.create(photo)  # type: Photo
            return photo.d()
        return Photo.get_random_photo()
