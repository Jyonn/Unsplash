from django.db import models


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

    @classmethod
    def create(cls, access_token):
        from Base.api import get_user_profile
        rtn = get_user_profile(access_token)
        if rtn is None:
            return None
        user_id = rtn['id']
        username = rtn['username']
        o_user = cls(
            user_id=user_id,
            username=username,
            access_token=access_token,
        )
        try:
            o_user.save()
            return o_user
        except:
            return None
