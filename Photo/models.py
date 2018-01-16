import random

from django.db import models

from Base.common import deprint
from Base.error import Error
from Base.response import Ret


class Photo(models.Model):
    L = {
        'photo_id': 20,
        'color': 10,
    }
    photo_id = models.CharField(
        max_length=L['photo_id'],
        unique=True,
    )
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(
        max_length=L['color'],
    )
    thumb = models.URLField(
        default=None,
    )
    small = models.URLField(
        default=None,
    )
    regular = models.URLField(
        default=None,
    )
    full = models.URLField(
        default=None,
    )
    raw = models.URLField(
        default=None,
    )
    create_time = models.DateTimeField(
        auto_created=True,
        auto_now=True,
    )

    @classmethod
    def create(cls, rtn):
        ret = cls.get_photo_by_id(rtn['id'])
        if ret.error is Error.OK:
            return Ret(Error.OK, ret.body)
        try:
            o_photo = cls(
                photo_id=rtn['id'],
                width=rtn['width'],
                height=rtn['height'],
                color=rtn['color'],
                thumb=rtn['urls']['thumb'],
                small=rtn['urls']['small'],
                regular=rtn['urls']['regular'],
                full=rtn['urls']['full'],
                raw=rtn['urls']['raw'],
            )
            o_photo.save()
        except:
            return Ret(Error.ERROR_CREATE_PHOTO)
        return Ret(Error.OK, o_photo)

    @classmethod
    def get_photo_by_id(cls, photo_id):
        try:
            o_photo = cls.objects.get(photo_id=photo_id)
        except Photo.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.PHOTO_NOT_FOUND)
        return Ret(Error.OK, o_photo)

    @classmethod
    def get_random_photo(cls):
        photos = cls.objects.all()
        index = random.randint(0, len(photos)-1)
        return photos[index].to_dict()

    def to_dict(self):
        return dict(
            color=self.color,
            thumb=self.thumb,
            small=self.small,
            regular=self.regular,
            full=self.full,
            raw=self.raw,
            width=self.width,
            height=self.height,
        )
