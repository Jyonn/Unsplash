import datetime

from Config.models import Config
from Photo.models import Photo


def clear_old_photo():
    try:
        last_time = float(Config.objects.get(key='last-clear-time').value)
    except:
        return
    crt_time = datetime.datetime.now().timestamp()
    last_datetime = datetime.datetime.fromtimestamp(last_time)
    if crt_time - last_time > 60 * 60 * 24:
        if len(Photo.objects.all()) > 1000:
            photos = Photo.objects.filter(create_time__lte=last_datetime)
            for photo in photos:
                photo.delete()
    return
