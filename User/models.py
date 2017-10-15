from django.db import models

from Base.error import Error
from Base.response import Ret


class User(models.Model):
    L = {
        'user_id': 20,
        'username': 20,
        'access_token': 64,
    }
    user_id = models.CharField(
        max_length=L['user_id'],
        primary_key=True,
    )
    username = models.CharField(
        max_length=L['username'],
        unique=True,
    )
    access_token = models.CharField(
        max_length=L['access_token'],
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
        from Base.api import get_user_profile
        rtn = get_user_profile(access_token)
        if rtn is None:
            return Ret(Error.ERROR_GET_PROFILE)
        user_id = rtn['id']
        username = rtn['username']
        email = rtn['email']
        try:
            o_user = cls.objects.get(pk=user_id)
            o_user.username = username
            o_user.email = email
            o_user.access_token = access_token
            o_user.expired = False
        except:
            o_user = cls(
                user_id=user_id,
                username=username,
                access_token=access_token,
                email=email,
                expired=False,
            )
        try:
            o_user.save()
            return Ret(Error.OK, o_user)
        except:
            return Ret(Error.USER_SAVE_ERROR)
