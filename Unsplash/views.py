from django.http import HttpResponseRedirect

from Base.api import get_access_token, get_random_photo, get_oauth_link
from Base.common import deprint
from Base.decorator import logging, require_get_params
from Base.error import Error
from Base.response import error_response, response
from User.models import User


@logging
@require_get_params(['code'])
def auth_callback(request):
    code = request.GET['code']
    deprint('CODE -- ', code)
    access_token = get_access_token(code)
    if access_token is None:
        return error_response(Error.ERROR_CODE)
    rtn = User.create(access_token)
    if rtn.error is not Error.OK:
        return error_response(rtn.error)
    return HttpResponseRedirect('/random')


@logging
def random(request):
    users = User.objects.all()
    for user in users:
        if not user.expired:
            rtn = get_random_photo(user.access_token)
            if rtn is None:
                user.expired = True
                user.save()
            else:
                return response(body=dict(
                    width=rtn['width'],
                    height=rtn['height'],
                    color=rtn['color'],
                    urls=rtn['urls'],
                ))
    return error_response(Error.NO_LEGAL_USER)


# @logging
def oauth(request):
    oauth_link = get_oauth_link()
    deprint(oauth_link)
    return HttpResponseRedirect(oauth_link)
