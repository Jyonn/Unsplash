from django.http import HttpResponseRedirect

from Base.api import get_access_token, get_random_photo, get_oauth_link
from Base.common import deprint
from Base.decorator import require_get
from Base.error import Error
from Base.response import error_response, response
from Base.rgb import RGB
from Base.similar_photo import SimilarPhoto
from Config.views import clear_old_photo
from Photo.models import Photo
from User.models import User


@require_get(['code'])
def auth_callback(request):
    code = request.d.code
    deprint('CODE -- ', code)
    access_token = get_access_token(code)
    if access_token is None:
        return error_response(Error.ERROR_CODE)
    rtn = User.create(access_token)
    if rtn.error is not Error.OK:
        return error_response(rtn.error)
    return HttpResponseRedirect('/random')


def random_empty(request):
    return random(request, 'regular')


@require_get([{
    "value": 'quick',
    "default": True,
    "default_value": 0,
    "process": int,
}])
def random(request, size):
    quick = request.d.quick
    if size not in ['thumb', 'small', 'regular', 'full', 'raw']:
        size = 'regular'
    if quick:
        return HttpResponseRedirect(Photo.get_random_photo()[size])
    users = User.objects.all()
    for user in users:
        if not user.expired:
            rtn = get_random_photo(user.access_token)
            if rtn is not None:
                clear_old_photo()
                Photo.create(rtn)
                return HttpResponseRedirect(rtn['urls'][size])
            else:
                return HttpResponseRedirect(Photo.get_random_photo()[size])
    return error_response(Error.NO_LEGAL_USER)


@require_get([{
    "value": 'quick',
    "default": True,
    "default_value": 0,
    "process": int,
}])
def random_info(request):
    quick = request.d.quick
    if quick:
        return response(body=Photo.get_random_photo())

    users = User.objects.all()
    for user in users:
        if not user.expired:
            rtn = get_random_photo(user.access_token)
            if rtn is not None:
                clear_old_photo()
                ret = Photo.create(rtn)
                if ret.error is Error.OK:
                    return response(body=ret.body.to_dict())
            break
    return response(body=Photo.get_random_photo())


@require_get()
def search(request, color):
    similar_photo = SimilarPhoto(10)
    o_rgb = RGB(color)
    for photo in Photo.objects.all():
        c2 = RGB(photo.color)
        dist = RGB.dist(o_rgb, c2)
        # print(o_rgb, c2, dist)
        # return response()
        similar_photo.push(dist, photo)
    search_list = [x[1].to_dict() for x in similar_photo.top()]
    return response(body=search_list)


def oauth(request):
    oauth_link = get_oauth_link()
    deprint(oauth_link)
    return HttpResponseRedirect(oauth_link)
