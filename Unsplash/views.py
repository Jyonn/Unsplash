from django.http import HttpResponseRedirect

from Base.api import get_access_token, get_random_photo, get_oauth_link
from Base.common import deprint
from Base.decorator import require_get
from Base.error import Error
from Base.response import error_response
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


def random(request, size):
    if size not in ['thumb', 'small', 'regular', 'full', 'raw']:
        size = 'regular'
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


def oauth(request):
    oauth_link = get_oauth_link()
    deprint(oauth_link)
    return HttpResponseRedirect(oauth_link)
