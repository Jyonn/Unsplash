import random
from urllib.parse import urlencode

import requests
import time

from SmartDjango import E, Hc

from Config.models import Config, CI
from Unsplash.settings import PROJ_INIT


@E.register(id_processor=E.idp_cls_prefix())
class AuthError:
    FAIL_CODE = E("获取授权码失败", hc=Hc.Unauthorized)
    GET_PROFILE = E("获取用户信息失败", hc=Hc.BadRequest)


if PROJ_INIT:
    UNSPLASH_CLIENT_ID = CI.UNSPLASH_CLIENT_ID
    UNSPLASH_SECRET = CI.UNSPLASH_SECRET
    UNSPLASH_REDIRECT_URI = CI.UNSPLASH_REDIRECT_URI
    UNSPLASH_HOST = CI.UNSPLASH_HOST
    UNSPLASH_API_HOST = CI.UNSPLASH_API_HOST
else:
    UNSPLASH_CLIENT_ID = Config.get_value_by_key(CI.UNSPLASH_CLIENT_ID)
    UNSPLASH_SECRET = Config.get_value_by_key(CI.UNSPLASH_SECRET)
    UNSPLASH_REDIRECT_URI = Config.get_value_by_key(CI.UNSPLASH_REDIRECT_URI)
    UNSPLASH_HOST = Config.get_value_by_key(CI.UNSPLASH_HOST)
    UNSPLASH_API_HOST = Config.get_value_by_key(CI.UNSPLASH_API_HOST)

UNSPLASH_AUTHORIZE_URI = UNSPLASH_HOST + '/oauth/authorize'
UNSPLASH_TOKEN_URI = UNSPLASH_HOST + '/oauth/token'
UNSPLASH_PROFILE_URI = UNSPLASH_API_HOST + '/me'
UNSPLASH_RANDOM_PHOTO_URI = UNSPLASH_API_HOST + '/photos/random'
UNSPLASH_OAUTH_URI = (f'{UNSPLASH_AUTHORIZE_URI}?'
                      f'client_id={UNSPLASH_CLIENT_ID}&'
                      f'redirect_uri={UNSPLASH_REDIRECT_URI}&'
                      f'response_type=code&scope=public+read_user')

random.seed(time.time())


class UnsplashAPI:
    @staticmethod
    def get_access_token(code):
        params = {
            'client_id': UNSPLASH_CLIENT_ID,
            'client_secret': UNSPLASH_SECRET,
            'redirect_uri': UNSPLASH_REDIRECT_URI,
            'code': code,
            'grant_type': 'authorization_code',
        }

        try:
            resp = requests.post(UNSPLASH_TOKEN_URI, json=params)
            if resp.status_code == 200:
                return resp.json()['access_token']
        except:
            raise AuthError.FAIL_CODE

    @staticmethod
    def get_user_profile(access_token):
        params = {
            'access_token': access_token,
        }
        params_encoded = urlencode(params)
        headers = {'content-type': 'application/json'}

        try:
            resp = requests.get(UNSPLASH_PROFILE_URI, params=params_encoded, headers=headers)
        except:
            raise AuthError.GET_PROFILE

        if resp.status_code == 200:
            return resp.json()
        raise AuthError.GET_PROFILE

    @staticmethod
    def get_random_photo(access_token):
        params = {
            'access_token': access_token,
        }
        params_encoded = urlencode(params)
        headers = {'content-type': 'application/json'}

        try:
            resp = requests.get(UNSPLASH_RANDOM_PHOTO_URI, params=params_encoded, headers=headers)
        except Exception as _:
            return None

        if resp.status_code == 200:
            return resp.json()
