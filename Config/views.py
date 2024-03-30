import datetime

from Config.models import Config, CI
from Photo.models import Photo


def clear_old_photo():
    try:
        last_time = Config.get_value_by_key(CI.LAST_CLEAR_TIME)
        last_time_value = float(last_time.value)
    except:
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
