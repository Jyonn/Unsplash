import datetime
import random

from diq import Dictify
from django.db import models

from Config.models import Config, CI
from Photo.validators import PhotoValidator, PhotoErrors


class Photo(models.Model, Dictify):
    vldt = PhotoValidator

    photo_id = models.CharField(
        max_length=vldt.MAX_PHOTO_ID_LENGTH,
        unique=True,
    )
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(
        max_length=vldt.MAX_COLOR_LENGTH,
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
    def create(cls, resp):
        photo = cls.get(resp['id'])
        if photo is not None:
            return photo

        photo = cls(
            photo_id=resp['id'],
            width=resp['width'],
            height=resp['height'],
            color=resp['color'],
            thumb=resp['urls']['thumb'],
            small=resp['urls']['small'],
            regular=resp['urls']['regular'],
            full=resp['urls']['full'],
            raw=resp['urls']['raw'],
        )

        try:
            photo.save()
        except Exception as e:
            raise PhotoErrors.CREATE(details=e)
        return photo

    @classmethod
    def get(cls, photo_id):
        try:
            return cls.objects.get(photo_id=photo_id)
        except Photo.DoesNotExist:
            pass
        # raise PhotoError.EXISTS
        return None

    @classmethod
    def get_random_photo(cls, size=None):
        photos = cls.objects.all()
        index = random.randint(0, len(photos)-1)
        photo = photos[index].d()
        if size:
            return photo[size]
        return photo

    @classmethod
    def get_random_photos(cls, num):
        photos = cls.objects.all()
        index_list = list(range(len(photos)))
        random.shuffle(index_list)
        index_list = index_list[:num]
        return [photos[i].d() for i in index_list]

    def d(self):
        return self.dictify('color', 'thumb', 'small', 'regular', 'full', 'raw', 'width', 'height')

    def __lt__(self, other):
        return False

    @classmethod
    def clear(cls):
        try:
            last_time = Config.get_value_by_key(CI.LAST_CLEAR_TIME)
            last_time_value = float(last_time.value)
        except Exception as _:
            return
        crt_time = datetime.datetime.now().timestamp()
        last_datetime = datetime.datetime.fromtimestamp(last_time_value)
        if crt_time - last_time_value > 60 * 60 * 24:
            if len(Photo.objects.all()) > 1000:
                photos = Photo.objects.filter(create_time__lte=last_datetime)
                for photo in photos:
                    photo.delete()
        last_time.value = crt_time
        last_time.save()
