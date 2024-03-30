import random

from SmartDjango import E, Hc, models


@E.register(id_processor=E.idp_cls_prefix())
class PhotoError:
    CREATE = E('创建图片失败', hc=Hc.InternalServerError)
    EXISTS = E('图片已存在', hc=Hc.BadRequest)


class Photo(models.Model):
    photo_id = models.CharField(
        max_length=20,
        unique=True,
    )
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(
        max_length=10,
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
        cls.exists(resp['id'])

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
            raise PhotoError.CREATE(debug_message=e)
        return photo

    @classmethod
    def exists(cls, photo_id):
        try:
            cls.objects.get(photo_id=photo_id)
        except Photo.DoesNotExist:
            return
        raise PhotoError.EXISTS

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
